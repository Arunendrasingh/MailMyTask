from django.urls import path, include
from todos import views

urlpatterns = [
    path("tasks/", view=views.ListCreateTodo.as_view(), name="Tasks"),
    path("tasks/<int:id>", views.GetUpdateDeleteTodo.as_view(), name="Task"),
    path("task_priority/", view=views.ListCreateTaskPriority.as_view(), name="Task-Priorities"),
    path("task_priority/<int:pk>", view=views.GetUpdateDeleteTaskPriority.as_view(), name="Task-Priority"),
    path("folders/", view=views.ListCreateFolder.as_view(), name="Folders"),
    path("folders/<int:pk>", view=views.GetUpdateDeleteFolder.as_view(), name="Folder"),
    path("sub_folders/", view=views.ListCreateSubFolder.as_view(), name="Sub-Folders"),
    path("sub_folders/<int:pk>", view=views.GetUpdateDeleteSubFolder.as_view(), name="Sub-Folder"),
    path("tags/", view=views.ListCreateTags.as_view(), name="Tags"),
    path("tags/<int:pk>", view=views.GetUpdateDeleteTags.as_view(), name="Tag"),
]
