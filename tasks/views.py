from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .permissions import IsOwnerOrAdmin
from .filters import TaskFilter


@extend_schema_view(
    list=extend_schema(
        description='Retrieve a list of all tasks for the authenticated user. Admins can see all tasks.',
        summary='List all tasks'
    ),
    retrieve=extend_schema(
        description='Retrieve details of a specific task by ID',
        summary='Get task details'
    ),
    create=extend_schema(
        description='Create a new task',
        summary='Create a task',
        request=TaskCreateSerializer
    ),
    update=extend_schema(
        description='Update all details of a specific task',
        summary='Update a task',
        request=TaskUpdateSerializer
    ),
    partial_update=extend_schema(
        description='Partially update details of a specific task',
        summary='Partially update a task',
        request=TaskUpdateSerializer
    ),
    destroy=extend_schema(
        description='Delete a specific task by ID',
        summary='Delete a task'
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model.
    
    Provides CRUD operations for tasks:
    - list: GET /tasks/
    - retrieve: GET /tasks/{id}/
    - create: POST /tasks/
    - update: PUT /tasks/{id}/
    - partial_update: PATCH /tasks/{id}/
    - destroy: DELETE /tasks/{id}/
    
    Additional endpoints:
    - completed: GET /tasks/completed/
    - incomplete: GET /tasks/incomplete/
    - mark_complete: POST /tasks/{id}/mark_complete/
    - mark_incomplete: POST /tasks/{id}/mark_incomplete/
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title', 'completed']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return tasks for the current user.
        Admin users can see all tasks.
        """
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.is_admin():
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """Save the task with the current user"""
        serializer.save(user=self.request.user)
    
    @extend_schema(
        description='Get all completed tasks',
        summary='List completed tasks'
    )
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed tasks"""
        queryset = self.get_queryset().filter(completed=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description='Get all incomplete tasks',
        summary='List incomplete tasks'
    )
    @action(detail=False, methods=['get'])
    def incomplete(self, request):
        """Get all incomplete tasks"""
        queryset = self.get_queryset().filter(completed=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        description='Mark a task as complete',
        summary='Mark task complete'
    )
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        """Mark a task as complete"""
        task = self.get_object()
        task.completed = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @extend_schema(
        description='Mark a task as incomplete',
        summary='Mark task incomplete'
    )
    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        """Mark a task as incomplete"""
        task = self.get_object()
        task.completed = False
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
