from django import forms
from django.contrib.auth.models import User
from .models import MypageProfile

class CombinedUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    nickname = forms.CharField(max_length=100, required=False)
    car_number = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = MypageProfile
        fields = ['file']  # MypageProfile의 필드만 포함

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super(CombinedUserProfileForm, self).__init__(*args, **kwargs)
        if user_instance:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['nickname'].initial = user_instance.nickname  # nickname 필드가 실제 User 모델에 없는 경우 커스텀 유저 모델에서 구현 필요
            self.fields['car_number'].initial = user_instance.car_number  # car_number 필드도 커스텀 필드로 가정
            self.fields['email'].initial = user_instance.email

    def save(self, commit=True):
        instance = super(CombinedUserProfileForm, self).save(commit=False)
        user_instance = instance.user

        user_instance.first_name = self.cleaned_data['first_name']
        user_instance.last_name = self.cleaned_data['last_name']
        user_instance.nickname = self.cleaned_data['nickname']  # 커스텀 유저 모델에서 구현 필요
        user_instance.car_number = self.cleaned_data['car_number']  # 커스텀 유저 모델에서 구현 필요
        user_instance.email = self.cleaned_data['email']

        if commit:
            user_instance.save()
            instance.save()

        return instance
