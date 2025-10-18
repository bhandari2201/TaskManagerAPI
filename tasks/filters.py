from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    """
    Filter set for Task model.
    
    Supports filtering by:
    - completed: Filter by completion status (true/false)
    - created_after: Filter tasks created after a specific date
    - created_before: Filter tasks created before a specific date
    - title: Filter by partial title match (case-insensitive)
    """
    completed = filters.BooleanFilter(field_name='completed')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    class Meta:
        model = Task
        fields = ['completed', 'created_after', 'created_before', 'title']

