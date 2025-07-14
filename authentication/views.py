from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User  
from .models import CustomUser

def index(request):
    return render(request, 'index.html')

def register_view(request):
    print('inside register view')
    if request.method == 'POST':
        print('in post method')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        print(f'username, {username}, password, {password}, contact, {contact}')

        if CustomUser.objects.filter(username=username).exists():
            print('user exists')
            messages.error(request, 'username already taken')
        else:
            print('inside else')
            user = CustomUser.objects.create(
                    username=username,
                    contact=contact
                )
            print('user',user)
            user.set_password(password)
            user.save()
            messages.info(request, 'user created successfully')
            print('created successflly')
            return redirect('user_login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username not found. Please register first')
        user = authenticate(username=username, password=password)
        print(user, 'checking activity')
        if user is None:
            messages.error(request, 'Invalid username or password')
        else:
            login(request, user)
            return render(request, 'index.html')
    return render(request, 'basic_login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return render(request, 'index.html')
