from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from todos.models import Todo

from datetime import datetime, timezone

# Your serializer

def convert_django_time_in_datetime(str_time: str):
    return datetime.strptime(str_time,  "%Y-%m-%dT%H:%M:%S.%fZ")

class TodoSerializer(serializers.ModelSerializer):

    # We can also create field level validator in ModelSerializer

    title = serializers.CharField(validators=[UniqueValidator(queryset=Todo.objects.all(), message="Title should be Unique.")])

    def validate(self, attrs):
        try:
            current_time = datetime.now(timezone.utc)

            time_diff  =  attrs["completion_time"] - current_time

            # if diff.days == 0 and diff.seconds == 0 : raise validation error to select greater time than current time.

            # if diff.days >= 0 and diff.
            if time_diff.day == 0 and time_diff.seconds == 0:
                return serializers.ValidationError("Todo time must be greater than current time.")
            
            if time_diff.day >= 0 and time_diff.seconds >= 0:
                return super().validate(attrs)
            
            return serializers.ValidationError("Todo time must be greater than current time.")
        except ValueError:
            return serializers.ValidationError("Please provide correct date-time format. accepted format is: '%Y-%m-%dT%H:%M:%S.%fZ'")

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.completion_time = validated_data.get('completion_time', instance.completion_time)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.reminder_before_time = validated_data.get('reminder_before_time', instance.reminder_before_time)
        instance.save()
        return instance
    class Meta:
        model = Todo
        fields = '__all__'

        