from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='signup'

urlpatterns = [
    path('', views.signup, name='signup'),
]
