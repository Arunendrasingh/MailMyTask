from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from todos.models import Todo

# Your serializer

class TodoSerializer(serializers.ModelSerializer):

    # We can also create field level validator in ModelSerializer

    title = serializers.CharField(validators=[UniqueValidator(queryset=Todo.objects.all(), message="Title should be Unique.")])

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


# class UpdateTodoSerializer(TodoSerializer):

#    class Meta:
        