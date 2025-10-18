from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
from accounts.models import UserProfile


class TaskModelTest(TestCase):
    """Test cases for Task model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user
        )
    
    def test_task_creation(self):
        """Test task is created correctly"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.user, self.user)
        self.assertFalse(self.task.completed)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
    
    def test_task_string_representation(self):
        """Test task string representation"""
        self.assertEqual(str(self.task), 'Test Task')


class TaskAPITest(APITestCase):
    """Test cases for Task API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123'
        )
        self.admin_user.profile.role = 'ADMIN'
        self.admin_user.profile.save()
        
        # Create another regular user
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Create tasks
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            user=self.user
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            completed=True,
            user=self.user
        )
        self.other_task = Task.objects.create(
            title='Other Task',
            description='Other Description',
            user=self.other_user
        )
        
        # Get JWT token for user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        # Get JWT token for admin
        admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(admin_refresh.access_token)
        
        # Get JWT token for other user
        other_refresh = RefreshToken.for_user(self.other_user)
        self.other_token = str(other_refresh.access_token)
    
    def test_list_tasks_unauthenticated(self):
        """Test listing tasks without authentication fails"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_tasks_authenticated(self):
        """Test listing tasks with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User should only see their own tasks
        self.assertEqual(response.data['count'], 2)
    
    def test_list_tasks_as_admin(self):
        """Test admin can see all tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin should see all tasks
        self.assertEqual(response.data['count'], 3)
    
    def test_retrieve_task(self):
        """Test retrieving a specific task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')
        self.assertEqual(response.data['description'], 'Description 1')
    
    def test_retrieve_other_user_task_fails(self):
        """Test user cannot retrieve another user's task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(f'/api/tasks/{self.other_task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_task(self):
        """Test creating a new task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'completed': False
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(Task.objects.count(), 4)
        # Verify the task was created for the correct user
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.user, self.user)
    
    def test_create_task_without_description(self):
        """Test creating a task without description"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'title': 'Task without description',
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_task_without_title_fails(self):
        """Test creating a task without title fails"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'description': 'Description without title',
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_task(self):
        """Test updating a task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'completed': True
        }
        response = self.client.put(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['completed'], True)
    
    def test_partial_update_task(self):
        """Test partially updating a task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'completed': True}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed'], True)
        self.assertEqual(response.data['title'], 'Task 1')  # Title unchanged
    
    def test_update_other_user_task_fails(self):
        """Test user cannot update another user's task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {'title': 'Hacked Task'}
        response = self.client.patch(f'/api/tasks/{self.other_task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_task(self):
        """Test deleting a task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=self.task1.id).count(), 0)
    
    def test_delete_other_user_task_fails(self):
        """Test user cannot delete another user's task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(f'/api/tasks/{self.other_task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_admin_can_update_any_task(self):
        """Test admin can update any user's task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        data = {'title': 'Admin Updated Task'}
        response = self.client.patch(f'/api/tasks/{self.other_task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Admin Updated Task')
    
    def test_filter_completed_tasks(self):
        """Test filtering completed tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/?completed=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 2')
    
    def test_filter_incomplete_tasks(self):
        """Test filtering incomplete tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/?completed=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')
    
    def test_search_tasks(self):
        """Test searching tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/?search=Task 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_completed_action(self):
        """Test completed tasks endpoint"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_incomplete_action(self):
        """Test incomplete tasks endpoint"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/incomplete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_mark_complete_action(self):
        """Test marking a task as complete"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(f'/api/tasks/{self.task1.id}/mark_complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])
    
    def test_mark_incomplete_action(self):
        """Test marking a task as incomplete"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(f'/api/tasks/{self.task2.id}/mark_incomplete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['completed'])
    
    def test_pagination(self):
        """Test pagination works"""
        # Create more tasks to test pagination
        for i in range(15):
            Task.objects.create(
                title=f'Task {i}',
                description=f'Description {i}',
                user=self.user
            )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # PAGE_SIZE is 10
