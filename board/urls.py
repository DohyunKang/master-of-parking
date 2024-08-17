from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('all/', views.board_all, name='board_all'),
   #path('<int:pk>/', views.board_detail, name='board_detail'),
    #path('board/', views.index, name='board'),
    #path('<int:question_id>/', views.detail),
]