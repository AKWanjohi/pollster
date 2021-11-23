from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import QuestionVoter, Topic, User, Question, QuestionVoter


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    topics = Topic.objects.all()[:5]

    polls = Question.objects.filter(
        Q(topic__name__icontains=q) | Q(question_text__icontains=q))
    polls_list = list(polls)

    if request.user.is_authenticated:
        voted_polls = QuestionVoter.objects.filter(voter=request.user).filter(
            Q(question__question_text__icontains=q) | Q(question__topic__name__icontains=q))
        for poll in voted_polls:
            if poll.question in polls_list:
                polls_list.remove(poll.question)
    else:
        voted_polls = []

    if voted_polls:
        if len(polls_list):
            polls_count = len(polls) - len(voted_polls)
        else:
            polls_count = 0
        context = {'topics': topics, 'polls': polls_list, 'voted_polls': voted_polls, 'all_polls': polls,
                   'polls_count': polls_count}
    else:
        context = {'topics': topics, 'polls': polls}

    return render(request, 'index.html', context)


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
