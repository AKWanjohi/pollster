from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Choice, QuestionVoter, Topic, User, Question, QuestionVoter


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    topics = Topic.objects.all()
    all_topics_count = 0
    for topic in topics:
        all_topics_count += len(topic.question_set.all())

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
                   'polls_count': polls_count, 'all_topics_count': all_topics_count}
    else:
        context = {'topics': topics, 'polls': polls,
                   'all_topics_count': all_topics_count}

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


@login_required(login_url='login')
def poll(request, poll_id):
    poll = Question.objects.get(id=poll_id)
    voted_poll = QuestionVoter.objects.filter(
        question=poll, voter=request.user)

    if request.method == 'POST':
        selected_choice = poll.choice_set.get(pk=request.POST.get('choice'))
        selected_choice.votes += 1
        selected_choice.save()

        poll.total_votes += selected_choice.votes
        poll.save()

        voter = QuestionVoter.objects.create(question=poll, voter=request.user)
        voter.save()

    context = {"poll": poll, 'voted_poll': voted_poll}
    return render(request, 'poll.html', context)


@login_required(login_url='login')
def create_poll(request):
    if request.method == "POST":
        poll_question = request.POST.get('poll_question')
        topic_name = request.POST.get('topic_name')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        poll_choices = []
        choices = request.POST.get('poll_choices')
        choices_list = choices.split(',')
        for choice in choices_list:
            poll_choices.append(choice.strip())

        question = Question.objects.create(
            creator=request.user, question_text=poll_question, topic=topic)
        question.save()

        for choice in poll_choices:
            choice = question.choice_set.create(choice_text=choice)
            choice.save()

        return redirect('home')
    topics = Topic.objects.all()
    return render(request, 'create_poll.html', {'topics': topics})


@login_required(login_url='login')
def profile(request, user_id):
    user = User.objects.get(pk=user_id)

    q = request.GET.get('q') if request.GET.get('q') != None else ""

    if request.user.is_authenticated:
        voted_polls = QuestionVoter.objects.filter(voter=request.user).filter(
            Q(question__question_text__icontains=q) | Q(question__topic__name__icontains=q))

    polls = Question.objects.filter(creator=user).filter(
        Q(topic__name__icontains=q) | Q(question_text__icontains=q))

    topics = Topic.objects.all()
    all_topics_count = 0
    for topic in topics:
        all_topics_count += len(topic.question_set.all())

    context = {'user': user, 'topics': topics,
               'polls': polls, 'voted_polls': voted_polls, 'all_topics_count': all_topics_count}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def profile_edit(request, user_id):
    if request.method == "POST":
        user_profile = User.objects.get(pk=user_id)
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.username = request.POST.get('username')
        user_profile.email = request.POST.get('email')
        user_profile.bio = request.POST.get('bio')
        user_profile.save()

        return redirect(profile, user_id=user_profile.id)
    user = User.objects.get(pk=user_id)
    context = {'user': user}
    return render(request, 'profile_edit.html', context)

def topics(request):
    topics = Topic.objects.all()
    all_topics_count = 0
    for topic in topics:
        all_topics_count += len(topic.question_set.all())
    
    context = {"topics": topics, "all_topics_count": all_topics_count}
    return render(request, 'topics.html', context)


def activities(request):
    if request.user.is_authenticated:
        voted_polls = QuestionVoter.objects.filter(voter=request.user)
        return render(request, 'activities.html', {"voted_polls": voted_polls})
        
    return render(request, 'activities.html')