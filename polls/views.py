from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User


def home(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Incorrect password.')
        except:
            messages.error(request, 'User does not exist')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username, email, password)
        try:
            user.save()
            auth_login(request, user)
            return redirect('home')
        except:
            messages.error(request, 'An error occurred during registration.')

    return render(request, 'register.html')


def logout(request):
    auth_logout(request)
    return redirect('home')
