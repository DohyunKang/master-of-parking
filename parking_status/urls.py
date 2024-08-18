from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
import os

app_name = 'parking_status'

urlpatterns = [
    path('parking_status/', views.parking_status, name='parking_status'),
    path('update_parking_data/', views.update_parking_data, name='update_parking_data'),
    path('get_parking_data/', views.get_parking_data, name='get_parking_data'),
]

# 이미지 서빙을 위한 URL 패턴 추가
urlpatterns += static('/img/', document_root=os.path.join(settings.BASE_DIR, 'parking_status', 'img'))
