"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from parking.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('bord/', include('board.urls')),
    path('parking_status/', include('parking_status.urls')),
    path('posts/', include('posts.urls')),
    path('posts2/', include('posts2.urls')),
    path('posts3/', include('posts3.urls')),
    path('mypage/', include('mypage.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/login/', include('login.urls')),
    path('signup/', include('signup.urls')),
    path('find/', include('find.urls')),
    path('chat/', include('chat.urls')),
    path('time_set/', include('timeset.urls')),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
]
