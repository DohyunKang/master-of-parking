from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name="login"

urlpatterns = [
    #path('', views.login, name='login'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]