from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=25, unique=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    content = models.TextField(null=False)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    priority = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
