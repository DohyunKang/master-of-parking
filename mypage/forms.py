from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'car_number']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'eg.example@sample.com'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Fill in your nickname'}),
            'car_number': forms.TextInput(attrs={'placeholder': 'Fill in your car number'}),
        }
