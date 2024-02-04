from django.contrib import admin
from todos.models import TaskPriority, Task, Tag, Folder, SubFolder
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskPriority)
admin.site.register(Tag)
admin.site.register(Folder)
admin.site.register(SubFolder)
