from django.urls import path, include
from todos import views

urlpatterns = [
    path("todos/", view=views.ListCreateTodo.as_view()),
    path("todos/<int:id>", views.GetUpdateDeleteTodo.as_view()),
]
