from django.shortcuts import render, get_object_or_404
from .models import Board

def board_all(request):
    return render(request, 'board/board_all.html')