from django import forms
from .models import TimeSet

class TimeSetForm(forms.ModelForm):
    class Meta:
        model = TimeSet
        fields = ['weekday', 'entry_time', 'exit_time']
