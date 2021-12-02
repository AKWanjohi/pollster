from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('poll/<int:poll_id>', views.poll, name='poll'),
    path('create-poll', views.create_poll, name='create-poll'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('profile-edit/<int:user_id>', views.profile_edit, name='profile-edit'),
]
