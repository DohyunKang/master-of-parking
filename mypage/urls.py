from django.urls import path
from . import views

app_name='mypage'

urlpatterns = [
    path('', views.mypage, name='mypage'),
    #path('change_password/', views.change_password, name='change_password'),
]