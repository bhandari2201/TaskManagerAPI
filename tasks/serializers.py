from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Includes all fields with read-only timestamps.
    """
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new task.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a task.
    All fields are optional for partial updates.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'completed': {'required': False},
        }

