from django.urls import path, include
from todos import views

urlpatterns = [
    path("", view=views.hello_world)
]
