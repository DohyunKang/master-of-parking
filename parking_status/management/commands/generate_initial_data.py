from django.core.management.base import BaseCommand
from django.utils import timezone
from parking_status.models import ParkingHistory  # 여기서 your_app을 실제 앱 이름으로 바꿈
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Generates initial parking history data for testing'

    def handle(self, *args, **kwargs):
        # 차량 번호판 리스트
        plate_texts = [
            "52다 3682",
            "23마 3562",
            "35우 9235",
            "68오 8269",
            "33라 6538",
            "56가 9683"
        ]

        # 요일별 초기 데이터 생성
        days_of_week = [0, 1, 2, 3, 4, 5, 6]  # 월요일부터 일요일까지
        today = timezone.now()
        one_month_ago = today - timedelta(weeks=4)  # 한 달 전

        for plate in plate_texts:
            for day in days_of_week:
                for week in range(4):  # 4주 동안의 데이터 생성
                    # 임의의 입차, 출차 시간 생성
                    entry_time = one_month_ago + timedelta(days=day + (week * 7), hours=random.randint(7, 9),
                                                           minutes=random.randint(0, 59))
                    exit_time = entry_time + timedelta(hours=random.randint(2, 6), minutes=random.randint(0, 59))

                    # ParkingHistory에 기록
                    ParkingHistory.objects.create(
                        plate_text=plate,
                        index=random.randint(1, 6),  # 1부터 6까지의 임의의 주차 공간 인덱스
                        entry_time=entry_time,
                        exit_time=exit_time
                    )

        self.stdout.write(self.style.SUCCESS('초기 데이터가 성공적으로 생성되었습니다.'))
