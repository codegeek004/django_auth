from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def callback(request):
    return render(request, 'callback.html')
