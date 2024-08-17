from django.urls import path
from . import views

app_name = 'parking_status'

urlpatterns = [
    path('parking_status/', views.parking_status, name='parking_status'),
    path('update_parking_data/', views.update_parking_data, name='update_parking_data'),
    path('get_parking_data/', views.get_parking_data, name='get_parking_data'),
]
