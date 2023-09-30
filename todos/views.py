from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from todos.serializers import TodoSerializer
from .models import Todo

# Create your views here.


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
        # TODO: First we have to create a serializer to serialize and deserialize the data to save or to return list of data.
        # Validating and saving user's todo data.

        todo_serializer = TodoSerializer(data=request.data)
        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(todo_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"hasError": True, "errors": todo_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

