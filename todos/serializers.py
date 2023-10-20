from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from todos.models import TaskPriority, Todo

from datetime import datetime, timezone

# Your serializer


def convert_django_time_in_datetime(str_time: str):
    return datetime.strptime(str_time,  "%Y-%m-%dT%H:%M:%S.%fZ")


class TodoSerializer(serializers.ModelSerializer):

    title = serializers.CharField(validators=[UniqueValidator(
        queryset=Todo.objects.all(), message="Title should be Unique.")])

    def validate(self, attrs):
        try:
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

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.completion_time = validated_data.get(
            'completion_time', instance.completion_time)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.reminder_before_time = validated_data.get(
            'reminder_before_time', instance.reminder_before_time)
        instance.save()
        return instance

    class Meta:
        model = Todo
        fields = '__all__'


class TaskPrioritySerializer(serializers.ModelSerializer):

    weight = serializers.IntegerField(validators=[UniqueValidator(
        queryset=TaskPriority.objects.all(), message="Weight should be Unique.")])
    
    title = serializers.CharField(validators=[UniqueValidator(
        queryset=TaskPriority.objects.all(), message="TaskPriority should be unique.")])

    class Meta:
        model = TaskPriority
        fields = '__all__'
