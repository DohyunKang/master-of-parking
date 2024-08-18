from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ParkingSpace, ParkingHistory
import json
from datetime import timedelta, datetime  # timedelta와 datetime을 가져옴
from collections import defaultdict
from timeset.models import TimeSet  # TimeSet 모델 import
from django.contrib.auth.models import User
from django.db.models import Avg, F
import os
from django.conf import settings

def parking_status(request):
    # 주차 상태 데이터 가져오기
    parking_spaces = ParkingSpace.objects.all()

    # 사용자별로 추천된 주차 공간 가져오기
    user = request.user
    if user.is_authenticated:
        car_number = user.car_number
        recommended_space = recommend_parking_space(car_number)
    else:
        recommended_space = None

    context = {
        'parking_spaces': parking_spaces,
        'recommended_space': recommended_space,  # 추천된 주차 공간 추가
    }

    return render(request, 'parking_status/parking_status.html', context)

def calculate_average_times():
    """요일별 평균 입차 시간, 출차 시간, 머무르는 시간 계산"""
    days_of_week = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    average_data = {}

    for i in range(7):
        histories = ParkingHistory.objects.filter(entry_time__week_day=i + 1)  # 1: 월요일, ..., 7: 일요일

        if histories.exists():
            total_entry_time = timedelta()
            total_exit_time = timedelta()
            total_duration = timedelta()
            count = histories.count()

            for history in histories:
                entry_time_of_day = history.entry_time.time()
                exit_time_of_day = history.exit_time.time()
                duration = history.exit_time - history.entry_time

                total_entry_time += timedelta(hours=entry_time_of_day.hour, minutes=entry_time_of_day.minute)
                total_exit_time += timedelta(hours=exit_time_of_day.hour, minutes=exit_time_of_day.minute)
                total_duration += duration

            average_entry_time = (total_entry_time / count).total_seconds()
            average_exit_time = (total_exit_time / count).total_seconds()
            average_duration = (total_duration / count).total_seconds()

            average_data[days_of_week[i]] = {
                'average_entry_time': str(timedelta(seconds=average_entry_time)),
                'average_exit_time': str(timedelta(seconds=average_exit_time)),
                'average_duration': str(timedelta(seconds=average_duration))
            }

    return average_data

def calculate_estimated_exit_time(plate_text):
    # 예시 알고리즘: 과거의 평균 주차 시간을 사용하여 예상 출차 시간을 계산
    history = ParkingHistory.objects.filter(plate_text=plate_text).order_by('-entry_time').first()
    if history:
        average_duration = ParkingHistory.objects.filter(plate_text=plate_text).aggregate(avg_duration=Avg(F('exit_time') - F('entry_time')))['avg_duration']
        if average_duration:
            return history.entry_time + average_duration
    return None

def get_user_exit_time(plate_text):
    try:
        user = User.objects.get(car_number=plate_text)
        current_weekday = timezone.now().strftime('%A')
        timeset = TimeSet.objects.get(user=user, weekday=current_weekday)
        return timeset.exit_time.strftime('%H:%M') if timeset.exit_time else '출차 시간 설정 안 됨'
    except TimeSet.DoesNotExist:
        return '출차 시간 설정 안 됨'
    except User.DoesNotExist:
        return '사용자 정보 없음'

def get_latest_image_url():
    image_dir = os.path.join(settings.BASE_DIR, 'parking_status', 'img')
    images = sorted(os.listdir(image_dir), key=lambda x: os.path.getctime(os.path.join(image_dir, x)), reverse=True)
    if images:
        return os.path.join('img', images[0])  # 가장 최근 이미지를 반환
    return None

@csrf_exempt
def update_parking_data(request):
    if request.method == 'POST':
        json_data = request.POST.get('json_data')
        if json_data:
            data = json.loads(json_data)

            existing_spaces = ParkingSpace.objects.all()
            space_dict = {space.index: space for space in existing_spaces}

            for plate in data.get('plates', []):
                plate_text = plate['plate_text']
                index = plate['index']
                current_time = timezone.now()

                if index in space_dict:
                    parking_space = space_dict[index]

                    # 차량이 다시 주차되었을 때 업데이트
                    if parking_space.is_occupied and parking_space.plate_text != plate_text:
                        # 새 차량으로 업데이트
                        parking_space.plate_text = plate_text
                        parking_space.entry_time = current_time
                        parking_space.exit_time = None
                        parking_space.save()

                        # ParkingHistory에 새로운 기록 추가
                        ParkingHistory.objects.create(
                            plate_text=plate_text,
                            index=index,
                            entry_time=current_time,
                            exit_time=None  # 종료 시 업데이트됩니다
                        )
                    # 기존 차량이 다시 주차된 경우
                    elif not parking_space.is_occupied:
                        parking_space.plate_text = plate_text
                        parking_space.is_occupied = True
                        parking_space.entry_time = current_time
                        parking_space.exit_time = None
                        parking_space.save()

                        # ParkingHistory에 새로운 기록 추가
                        ParkingHistory.objects.create(
                            plate_text=plate_text,
                            index=index,
                            entry_time=current_time,
                            exit_time=None  # 종료 시 업데이트됩니다
                        )

            # 빈 주차 공간 업데이트
            for free_space in data.get('free', []):
                index = free_space['free']
                if index in space_dict:
                    parking_space = space_dict[index]
                    if parking_space.is_occupied:
                        parking_space.exit_time = current_time
                        parking_space.is_occupied = False
                        parking_space.save()

                        # 출차 시간 업데이트
                        last_history = ParkingHistory.objects.filter(
                            plate_text=parking_space.plate_text,
                            index=index
                        ).last()
                        if last_history:
                            last_history.exit_time = current_time
                            last_history.save()

        # 이미지가 업로드된 경우, 이를 저장합니다.
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image_dir = os.path.join(settings.BASE_DIR, 'parking_status', 'img')
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, f'image_{timezone.now().strftime("%Y%m%d_%H%M%S")}.png')

            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            print(f"Image saved as {image_path}")

        return JsonResponse({"status": "success"})

    return HttpResponseNotAllowed(['POST'])

def update_parking_history():
    # 출차가 감지된 차량을 ParkingHistory에 기록
    for space in ParkingSpace.objects.filter(is_occupied=True):
        if condition_for_exit(space):  # condition_for_exit는 출차를 감지하는 로직
            space.exit_time = timezone.now()
            space.save()

            # ParkingHistory에 기록
            ParkingHistory.objects.create(
                plate_text=space.plate_text,
                index=space.index,
                entry_time=space.entry_time,
                exit_time=space.exit_time
            )

            # 주차 공간을 빈 공간으로 설정
            space.is_occupied = False
            space.plate_text = None
            space.entry_time = None
            space.exit_time = None
            space.save()

def get_parking_data(request):
    parking_data = list(ParkingSpace.objects.all().values().order_by('index'))  # 인덱스로 정렬
    history_data = list(ParkingHistory.objects.all().values())

    # 요일별 평균 계산
    average_times = calculate_average_times()

    # 오늘의 입차 시간
    today_entry_times = []
    for parking in parking_data:
        if parking['is_occupied']:
            today_entry_times.append(parking['entry_time'])

            # 예상 출차 시간 계산
            estimated_exit_time = calculate_estimated_exit_time(parking['plate_text'])
            parking['estimated_exit_time'] = estimated_exit_time.strftime('%H:%M') if estimated_exit_time else "출차 시간 계산되지 않음"

            # 출차 설정 시간 가져오기
            user_exit_time = get_user_exit_time(parking['plate_text'])
            parking['user_exit_time'] = user_exit_time if user_exit_time else '출차 시간 설정 안 됨'

    # 추천된 주차 공간 인덱스를 포함하여 반환
    recommended_space = None
    user = request.user
    if user.is_authenticated:
        car_number = user.car_number
        recommended_space = recommend_parking_space(car_number)
        if recommended_space:
            recommended_index = recommended_space.index
        else:
            recommended_index = None
    else:
        recommended_index = None

    # 가장 최근 이미지의 URL 가져오기
    image_url = get_latest_image_url()

    return JsonResponse({
        "parking": parking_data,
        "history": history_data,
        "average_times": average_times,
        "today_entry_times": today_entry_times,
        "recommended_space_index": recommended_index,
        "image_url": image_url
    })

def recommend_parking_space(plate_text):
    # 특정 차량의 과거 주차 패턴 분석
    histories = ParkingHistory.objects.filter(plate_text=plate_text)

    # 주차 공간별로 점수를 매기기 위한 딕셔너리
    score_dict = defaultdict(int)

    for history in histories:
        # 주차된 인덱스에 대해 점수 부여
        score_dict[history.index] += 1

        # 주차된 요일에 대해 가중치 부여
        weekday = history.entry_time.weekday()
        score_dict[history.index] += weekday

        # 주차 시간의 패턴에 따라 가중치 부여 (예: 출퇴근 시간대)
        entry_hour = history.entry_time.hour
        if 7 <= entry_hour <= 9 or 17 <= entry_hour <= 19:
            score_dict[history.index] += 2

    # 모든 주차 공간의 리스트 가져오기
    all_spaces = ParkingSpace.objects.all()

    # 주차공간이 비어있지 않은 경우에도 점수를 고려하여 추천
    recommended_space = None
    max_score = -1

    for space in all_spaces:
        # 점유되지 않은 주차공간만 고려
        if not space.is_occupied:
            space_score = score_dict.get(space.index, 0)
            if space_score > max_score:
                recommended_space = space
                max_score = space_score

    # 만약 최적의 주차 공간을 찾지 못한 경우, 첫 번째 빈 주차 공간을 반환
    if recommended_space is None:
        recommended_space = all_spaces.filter(is_occupied=False).first()

    return recommended_space
