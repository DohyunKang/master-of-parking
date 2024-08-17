from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    #path('create_posts/', views.create_posts, name='create_posts'),
    #path('view_posts/', views.view_posts, name='view_posts'),
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name="detail"),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
    path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
]