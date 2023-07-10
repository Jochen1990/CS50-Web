from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="author")
    question = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField(blank=True)
    answer4 = models.TextField(blank=True)
    timestamp = models.DateTimeField()
    archived = models.BooleanField (default=False)

class Vote(models.Model):
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1', related_name="voter")
    answer = models.TextField()
