from django.shortcuts import render, redirect

def index(request):
    return render(request, 'home/index.html')
def before_index(request):
    return render(request, 'home/before_index.html')

def nearby_parking(request):
    return render(request, 'home/nearby_parking.html')