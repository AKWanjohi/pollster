from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, SET_NULL


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    creator = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    question_text = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=CASCADE)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class QuestionVoter(models.Model):
    question = models.ForeignKey(Question, on_delete=CASCADE)
    voter = models.ForeignKey(User, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.question.question_text
