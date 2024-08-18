from django.db import models
from django.contrib.auth.models import User

class MypageProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mypage_profile')
    file = models.FileField(upload_to='profile_pics/', blank=True, null=True)  # file 필드를 사용

    def __str__(self):
        return f'{self.user.username} MypageProfile'
