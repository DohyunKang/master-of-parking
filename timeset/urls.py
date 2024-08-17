from django.urls import path
from . import views

app_name = 'time_set'

urlpatterns = [
    path('set/', views.set_time, name='set_time'),
    path('reset/', views.reset_times, name='reset_times'),
]
