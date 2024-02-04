from django_filters import rest_framework as filters

from todos.models import Task

# Your Filter Class


class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='iexact')
    task_priority__title = filters.CharFilter(lookup_expr='icontains')
    sub_folder__title = filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Task
        fields = ['title', 'task_priority', 'sub_folder']

    