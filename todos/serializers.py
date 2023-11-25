from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from todos.models import TaskPriority, Todo

from datetime import datetime, timezone

# Your serializer


def convert_django_time_in_datetime(str_time: str):
    return datetime.strptime(str_time,  "%Y-%m-%dT%H:%M:%S.%fZ")

class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=TaskPriority.objects.all(), fields=["title", "user"]),
            UniqueTogetherValidator(queryset=TaskPriority.objects.all(), fields=["weight", "user"]),
        ]


class TodoSerializer(serializers.ModelSerializer):
    task_priority = TaskPrioritySerializer(read_only=True)
    
    class Meta:
        model = Todo
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(queryset=Todo.objects.all(), fields=["title", "user"])
        ]


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

    def validate(self, attrs):
        try:
            if not attrs.get("completion_time"):
                return super().validate(attrs)
            current_time = datetime.now(timezone.utc)

            time_diff = attrs["completion_time"] - current_time

            if time_diff.days == 0 and time_diff.seconds == 0:
                return serializers.ValidationError("Todo time must be greater than current time.")

            if time_diff.days >= 0 and time_diff.seconds >= 0:
                return super().validate(attrs)

            raise serializers.ValidationError(
                "Todo time must be greater than current time.")
        except ValueError:
            raise serializers.ValidationError(
                "Please provide correct date-time format. accepted format is: '%Y-%m-%dT%H:%M:%S.%fZ'")


