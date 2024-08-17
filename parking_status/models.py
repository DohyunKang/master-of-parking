from django.db import models
from django.utils import timezone

class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    available_spots = models.IntegerField()

    def __str__(self):
        return self.name

class ParkingSpace(models.Model):
    plate_text = models.CharField(max_length=20, null=True, blank=True)  # 번호판 텍스트, 빈 공간일 경우 None
    index = models.IntegerField()  # 주차 공간 인덱스
    entry_time = models.DateTimeField(null=True, blank=True)  # 입차 시간, 빈 공간일 경우 None
    exit_time = models.DateTimeField(null=True, blank=True)  # 출차 시간, 빈 공간일 경우 None
    is_occupied = models.BooleanField(default=False)  # 주차 상태 (True: 주차됨, False: 빈 공간)

    def __str__(self):
        if self.is_occupied:
            return f"ParkingSpace {self.index}: {self.plate_text} (Occupied)"
        else:
            return f"ParkingSpace {self.index}: (Free)"

class ParkingHistory(models.Model):
    plate_text = models.CharField(max_length=20)
    index = models.IntegerField()
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()

    def __str__(self):
        return f"ParkingHistory {self.index}: {self.plate_text}"