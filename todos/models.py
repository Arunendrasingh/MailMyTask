from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class SubFolder(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(blank=True)
    completion_time = models.DateTimeField()
    reminder = models.BooleanField(default=False)
    reminder_before_time = models.IntegerField()
    task_priority = models.ForeignKey(
        "TaskPriority", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class TaskPriority(models.Model):
    title = models.CharField(max_length=90)
    color = models.CharField(max_length=20)
    weight = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedAt = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
