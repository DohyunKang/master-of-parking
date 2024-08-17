from django.shortcuts import render

def find(request):
    return render(request, 'find/find.html')
