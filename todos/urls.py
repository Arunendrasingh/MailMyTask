from django.urls import path, include
from todos import views

urlpatterns = [
    path("todos/", view=views.ListCreateTodo.as_view()),
    path("todos/<int:id>", views.GetUpdateDeleteTodo.as_view()),
    path("task_priority/", view=views.ListCreateTaskPriority.as_view()),
    path("task_priority/<int:pk>", view=views.GetUpdateDeleteTaskPriority.as_view()),
    path("folders/", view=views.ListCreateFolder.as_view()),
    path("folders/<int:pk>", view=views.GetUpdateDeleteFolder.as_view()),
    path("sub_folders/", view=views.ListCreateSubFolder.as_view()),
    path("sub_folders/<int:pk>", view=views.GetUpdateDeleteSubFolder.as_view()),
]
