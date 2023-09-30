from django.db import models



class Todo(models.Model):
    title =  models.CharField(max_length=90)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50) #  Need to use DropDown and also need to create Priority table in database to priorities the task.
    completion_time = models.DateTimeField()
    reminder = models.BooleanField(default=False)
    reminder_before_time = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_At = models.DateTimeField(auto_now_add=True)