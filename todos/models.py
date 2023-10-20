from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50)
    completion_time = models.DateTimeField()
    reminder = models.BooleanField(default=False)
    reminder_before_time = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_At = models.DateTimeField(auto_now_add=True)
    task_priority = models.ForeignKey("TaskPriority", null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title


class TaskPriority(models.Model):
    title = models.CharField(max_length=90)
    color = models.CharField(max_length=20)
    weight = models.IntegerField()

    def __str__(self) -> str:
        return self.title
    

# TODO: Fix AttributeError: 'datetime.timedelta' object has no attribute 'day' error in Code By Tomorrow.
