from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('poll/<int:poll_id>', views.poll, name='poll'),
    path('poll/<int:poll_id>/results', views.results, name='results'),
    path('create-poll', views.create_poll, name='create-poll'),
]
