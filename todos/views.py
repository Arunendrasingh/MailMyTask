from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from todos.serializers import TaskPrioritySerializer, TodoSerializer
from .models import TaskPriority, Todo

# Create your views here.

# TODO: Add logger in python to log all request and request and response to validate any error and anything. do it after completing  this project.


class ListCreateTodo(APIView):
    """
    This View create a new todo in db on Post request and return list of todo's for Get request.
    """

    def get(self, request):
        """
        Return a list of all todos.
        """
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        if not todos:
            return Response({"value": [], "error": True, "status": "No todo is available "})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        this method create new todo in db.

        """
        todo_serializer = TodoSerializer(data=request.data)
        if todo_serializer.is_valid(raise_exception=True):
            todo_serializer.save()
            return Response(todo_serializer.data, status=status.HTTP_201_CREATED)

        return Response({"hasError": True, "errors": todo_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDeleteTodo(APIView):
    """
    This views use to retrieve  a single todo with id, and it will be also used to update and delete a todo with id
    """

    def get(self, request, id):
        todo = Todo.objects.filter(id=id).first()
        if not todo:
            return Response({"hasError": True, "errors": "Requested object is not in found.", "value": []}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo)
        return Response({"hasError": False, "value": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        todo = Todo.objects.filter(id=id).first()
        if not todo:
            return Response({"hasError": True, "errors": "Requested object is not in found.", "value": []}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(
            instance=todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        todo_to_delete = Todo.objects.filter(id=id).first()
        if not todo_to_delete:
            return Response({"hasError": True, "errors": f"No TODO is present to delete with id: {id}", "value": []}, status=status.HTTP_404_NOT_FOUND)

        todo_to_delete.delete()

        return Response({"hasError": False, "messages": f"TODO with id: {id} is deleted."}, status=status.HTTP_200_OK)


class ListCreateTaskPriority(APIView):
    """This class is used to create a task Priority or to get a list of task priority."""

    def post(self, request):
        """This method get a post request and create a new task priority if not already created."""
        # Now add code to get the value from request.
        task_priority_serializer = TaskPrioritySerializer(data=request.data)

        if task_priority_serializer.is_valid(raise_exception=True):
            task_priority_serializer.save()
            return Response({
                "hasError": False,
                "errors": "",
                "resultObject": task_priority_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "hasError": True,
            "errors": task_priority_serializer.errors,
            "resultObject": None
        })

    def get(self, request):
        """this method accept a get request and return a list of taskpriority"""
        task_priority = TaskPriority.objects.all()
        task_priority_serializer = TaskPrioritySerializer(
            task_priority, many=True)

        if not task_priority_serializer:
            return Response({
                "hasError": True,
                "errors": task_priority_serializer.errors,
                "resultObject": []
            })

        return Response({
            "hasError": False,
            "errors": "",
            "resultObject": task_priority_serializer.data
        })


class GetUpdateDeleteTaskPriority(APIView):
    def get(self, request, task_priority_id):
        todo = TaskPriority.objects.filter(id=task_priority_id).first()
        if not todo:
            return Response({"hasError": True, "errors": "Requested object is not in found.", "resultObject": {}}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskPrioritySerializer(todo)
        return Response({"hasError": False, "errors": None, "resultObject": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, task_priority_id):
        todo = TaskPriority.objects.filter(id=task_priority_id).first()
        if not todo:
            return Response({"hasError": True, "errors": "Requested object is not in found.", "resultObject": {}}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskPrioritySerializer(
            instance=todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"hasError": False, "errors": serializer.errors, "resultObject": serializer.data}, status=status.HTTP_200_OK)

        return Response({"hasError": True, "errors": serializer.errors, "resultObject": {}}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        todo_to_delete = TaskPriority.objects.filter(id=id).first()
        if not todo_to_delete:
            return Response({"hasError": True, "errors": f"No TaskPriority to delete with id: {id}", "resultObject": None}, status=status.HTTP_404_NOT_FOUND)

        todo_to_delete.delete()

        return Response({"hasError": False, "messages": f"Task Priority with id: {id} is deleted."}, status=status.HTTP_200_OK)
