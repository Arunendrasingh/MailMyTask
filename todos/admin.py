from django.contrib import admin
from todos.models import TaskPriority, Task
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskPriority)
