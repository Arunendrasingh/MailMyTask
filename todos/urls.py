from django.urls import path, include
from todos import views

urlpatterns = [
    path("todos/", view=views.ListCreateTodo.as_view())
]
