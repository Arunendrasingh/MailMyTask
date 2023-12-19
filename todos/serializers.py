from rest_framework import serializers
from todos.models import Folder, SubFolder, TaskPriority, Todo

from datetime import datetime, timezone

# Your serializer


def convert_django_time_in_datetime(str_time: str):
    return datetime.strptime(str_time,  "%Y-%m-%dT%H:%M:%S.%fZ")


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        exclude = ["user"]

    def validate_title(self, value):
        request = self.context["request"]

        if TaskPriority.objects.filter(user=request.user, title=value).exists():
            raise serializers.ValidationError(
                f"A Task priority with title '{value}' is already present.")

        return value

    def validate_weight(self, value):
        request = self.context["request"]

        if TaskPriority.objects.filter(user=request.user, weight=value).exists():
            raise serializers.ValidationError(
                f"A Task priority with weight '{value}' is already present.")

        return value


class TodoSerializer(serializers.ModelSerializer):
    task_priority = TaskPrioritySerializer(read_only=True)
    owner = serializers.CharField(source="user", read_only=True)

    class Meta:
        model = Todo
        fields = ["id", "title", "description", "reminder", "reminder_before_time",
                  "completion_time",  "task_priority", "owner", "updatedAt", "createdAt"]

    def validate_task_priority(self, value):
        # get the existence of value in Priority table
        if not value:
            return None

        if isinstance(value, TaskPriority):
            value = value.id

        priority = TaskPriority.objects.filter(id=value).first()
        if priority:
            return priority

        raise serializers.ValidationError(
            "Unable to find validation with key: ", value)

    def validate_title(self, value):
        if Todo.objects.filter(title__iexact=value, user=self.context["request"].user).exists():
            raise serializers.ValidationError(
                f"A Task with title '{value}' is already exists.")

        return value

    def validate_completion_time(self, value):
        try:
            current_time = datetime.now(timezone.utc)

            time_diff = value - current_time

            if time_diff.days == 0 and time_diff.seconds == 0:
                return serializers.ValidationError("Todo time must be greater than current time.")

            if time_diff.days >= 0 and time_diff.seconds >= 0:
                return value

            raise serializers.ValidationError(
                "Todo time must be greater than current time.")
        except ValueError:
            raise serializers.ValidationError(
                "Please provide correct date-time format. accepted format is: '%Y-%m-%dT%H:%M:%S.%fZ'")


class FolderSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="user", read_only=True)

    class Meta:
        model = Folder
        fields = ["id", "title", "description",
                  "owner", "updatedAt", "createdAt"]

    def validate_title(self, value):
        request = self.context["request"]
        if Folder.objects.filter(user=request.user, title=value).exists():
            raise serializers.ValidationError(
                f"Folder with name '{value}' already present.")

        return value


class SubFolderSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="user", read_only=True)
    folder = FolderSerializer(read_only=True)
    folder_id = serializers.CharField(source="folder", write_only=True)

    class Meta:
        model = SubFolder
        fields = ["id", "title", "description", "folder", "folder_id",
                  "owner", "updatedAt", "createdAt"]

    def validate_title(self, value):
        request = self.context["request"]
        if SubFolder.objects.filter(user=request.user, title=value).exists():
            raise serializers.ValidationError(
                f"Folder with name '{value}' already present.")

        return value

    def validate_folder_id(self, value):
        # get the existence of value in Priority table
        request = self.context["request"]
        if not value:
            raise serializers.ValidationError(
                "ID of folder is required to Create/Update the Sub Folder")

        if isinstance(value, Folder):
            value = value.id

        priority = Folder.objects.filter(id=value, user=request.user).first()
        if priority:
            return priority

        raise serializers.ValidationError(
            f"Unable to find folder with key: {value}")
