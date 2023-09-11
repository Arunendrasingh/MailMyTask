from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def hello_world(request):
    return JsonResponse({"value": "Hello World, I am first API in Django Rest", "status":True})
