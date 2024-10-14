# questions/models.py

from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    step = models.IntegerField(default=0)

    def __str__(self):
        return self.tag_name

class Question(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Changed to ForeignKey

    def __str__(self):
        return self.question


class FavoriteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class ReadQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null temporarily
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

