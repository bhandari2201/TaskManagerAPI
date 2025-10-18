from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Task model representing a task in the task manager.
    
    Fields:
        id: Auto-generated primary key
        title: Title of the task
        description: Detailed description of the task
        completed: Boolean indicating if the task is completed
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
        user: Foreign key to the User who owns the task
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['completed']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return self.title
