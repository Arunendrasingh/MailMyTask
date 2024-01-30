import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from MailMyTask.custom_response import CustomResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.renderers import BrowsableAPIRenderer
from drf_spectacular.utils import extend_schema

from todos.serializers import FolderSerializer, SubFolderSerializer, TaskPrioritySerializer, TodoSerializer
from MailMyTask.custom_renderer import CustomRenderer
from .models import Folder, SubFolder, TaskPriority, Todo

# Create your views here.

# logger
logger = logging.getLogger("django")


class ListCreateTodo(APIView):
    """
    This View create a new todo in db on Post request and return list of todo's for Get request.
    """

    permission_classes = [IsAuthenticated]
    filter_set = ["title", "completion_time", "reminder",
                  "sub_folder__title", "task_priority__title"]

    @extend_schema(request=TodoSerializer, responses=TodoSerializer)
    def get(self, request):
        """
        Return a list of all todos.
        """
        # Query params
        # Printing auth and user
        print("Query Parameters: ", request.query_params)
        print("Query Parameters Title: ", request.query_params.get(
            "title"), type(request.query_params.get("title")))
        filter_perm = {s: request.query_params.get(
            s) for s in self.filter_set if request.query_params.get(s)}
        print("Filter set on Query parameter", filter_perm)
        # Query parameters.
        todos = Todo.objects.filter(user=request.user)
        todos = todos.filter(**filter_perm)
        serializer = TodoSerializer(
            todos, many=True, context={"request": request})

        if not todos:
            logger.warning("No Todo object present.")
            return CustomResponse(has_error=True, errors="No Task is available.")

        logger.info("Returning List of todo.")
        return CustomResponse(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=TodoSerializer, responses=TodoSerializer)
    def post(self, request):
        """
        this method create new todo and add a task to send email before the scheduled time as per user's reminder detail..

        """
        logger.info("Creating new Todo")
        todo_serializer = TodoSerializer(
            data=request.data, context={"request": request})

        if todo_serializer.is_valid():
            todo_obj: Todo = todo_serializer.save(user_id=request.user.id)
            todo_obj.schedule_email()
            return CustomResponse(todo_serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(
            f"Failed to create Todo due to error: {todo_serializer.errors}")
        return CustomResponse(has_error=True, errors=todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateDeleteTodo(APIView):
    """
    This views use to retrieve  a single todo with id, and it will be also used to update and delete a todo with id
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(request=TodoSerializer, responses=TodoSerializer)
    def get(self, request, id):
        todo = Todo.objects.filter(id=id, user=request.user).first()
        if not todo:
            return CustomResponse(has_error=True, errors="Requested object is not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, context={"request": request})
        return CustomResponse(has_error=False, data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=TodoSerializer, responses=TodoSerializer)
    def put(self, request, id):
        todo = Todo.objects.filter(id=id, user=request.user).first()
        if not todo:
            return CustomResponse(has_error=True, errors="Requested object is not found.", data=[], status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(
            instance=todo, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            todo_obj: Todo = serializer.save()
            # Rescheduling the email by revoking existing task.
            todo_obj.update_schedule_email()
            return CustomResponse(serializer.data, has_error=False)

        return CustomResponse(has_error=True, errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=None, responses=None)
    def delete(self, request, id):
        todo_to_delete = Todo.objects.filter(id=id, user=request.user).first()
        if not todo_to_delete:
            return CustomResponse(has_error=True, errors=f"No Task is present to delete with id: {id}", data=[], status=status.HTTP_404_NOT_FOUND)

        todo_to_delete.delete()

        return CustomResponse(has_error=False, data=f"Task with id: {id} is deleted.", status=status.HTTP_200_OK)


class ListCreateTaskPriority(ListCreateAPIView):
    """This class is used to create a task Priority or to get a list of task priority."""

    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = TaskPriority.objects.all()
    serializer_class = TaskPrioritySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetUpdateDeleteTaskPriority(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = TaskPriority.objects.all()
    serializer_class = TaskPrioritySerializer


# Views for Folders and SubFolder.

class ListCreateFolder(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class GetUpdateDeleteFolder(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class ListCreateSubFolder(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = SubFolder.objects.all()
    serializer_class = SubFolderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class GetUpdateDeleteSubFolder(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    queryset = SubFolder.objects.all()
    serializer_class = SubFolderSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
