from django.db import models
from django.contrib.auth.models import User

class TimeSet(models.Model):
    WEEKDAYS = [
        ('Monday', '월요일'),
        ('Tuesday', '화요일'),
        ('Wednesday', '수요일'),
        ('Thursday', '목요일'),
        ('Friday', '금요일'),
        ('Saturday', '토요일'),
        ('Sunday', '일요일'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    entry_time = models.TimeField(blank=True, null=True)
    exit_time = models.TimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'weekday')

    def __str__(self):
        return f'{self.user.username} - {self.weekday}'
