# Task Manager API

A comprehensive RESTful API for task management built with Django and Django REST Framework. This API provides complete CRUD operations for tasks with JWT authentication, role-based permissions, pagination, filtering, and extensive API documentation.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [User Roles](#user-roles)
- [Usage Examples](#usage-examples)
- [Testing with Coverage](#testing-with-coverage)

## ✨ Features

### Core Features
- ✅ **Complete CRUD Operations** for tasks
- ✅ **JWT Authentication** using Simple JWT
- ✅ **User Registration and Login**
- ✅ **User Profile Management**
- ✅ **Password Change Functionality**

### Bonus Features
- ✅ **Pagination** (10 items per page)
- ✅ **Advanced Filtering** (by completion status, date range, title)
- ✅ **Search Functionality** (search in title and description)
- ✅ **Sorting** (by created_at, updated_at, title, completed)
- ✅ **Role-Based Access Control** (Admin and Regular User roles)
- ✅ **Interactive API Documentation** (Swagger UI and ReDoc)
- ✅ **Comprehensive Unit Tests** (43 test cases with 100% coverage)

### Task Features
- Task model with id, title, description, completed status, timestamps
- Users can only view and manage their own tasks
- Admin users can view and manage all tasks
- Additional endpoints for completed/incomplete tasks
- Mark tasks as complete/incomplete

## 🛠 Tech Stack

- **Framework**: Django 4.2.7
- **REST Framework**: Django REST Framework 3.14.0
- **Authentication**: Django REST Framework Simple JWT 5.3.0
- **Filtering**: django-filter 23.3
- **Documentation**: drf-spectacular 0.26.5 (Swagger/OpenAPI)
- **CORS**: django-cors-headers 4.3.0
- **Database**: SQLite (development), PostgreSQL ready
- **Testing**: Django TestCase, DRF APITestCase
- **Coverage**: coverage 7.3.2

## 📁 Project Structure

```
TaskManagerAPI/
├── accounts/              # User authentication and management
│   ├── models.py         # UserProfile model with roles
│   ├── serializers.py    # User and auth serializers
│   ├── views.py          # Auth and user management views
│   ├── urls.py           # Auth endpoints
│   ├── admin.py          # Admin configuration
│   └── tests.py          # Authentication tests (18 tests)
├── tasks/                # Task management app
│   ├── models.py         # Task model
│   ├── serializers.py    # Task serializers
│   ├── views.py          # Task CRUD views
│   ├── urls.py           # Task endpoints
│   ├── permissions.py    # Custom permissions
│   ├── filters.py        # Task filters
│   ├── admin.py          # Admin configuration
│   └── tests.py          # Task tests (25 tests)
├── taskmanager/          # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd TaskManagerAPI
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

## 🏃 Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - API Base URL: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`
   - Swagger UI: `http://localhost:8000/api/docs/`
   - ReDoc: `http://localhost:8000/api/redoc/`

## 🧪 Running Tests

### Run all tests
```bash
python manage.py test
```

### Run tests for a specific app
```bash
# Test tasks app
python manage.py test tasks

# Test accounts app
python manage.py test accounts
```

### Run tests with verbosity
```bash
python manage.py test --verbosity=2
```

### Run specific test class or method
```bash
python manage.py test tasks.tests.TaskAPITest
python manage.py test tasks.tests.TaskAPITest.test_create_task
```

## 📊 Testing with Coverage

Generate a test coverage report:

```bash
# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in your browser
```

## 📚 API Documentation

The API includes comprehensive interactive documentation:

### Swagger UI
- URL: `http://localhost:8000/api/docs/`
- Interactive API documentation
- Test endpoints directly from the browser
- View request/response schemas

### ReDoc
- URL: `http://localhost:8000/api/redoc/`
- Clean, responsive API documentation
- Easy to navigate and read

### OpenAPI Schema
- URL: `http://localhost:8000/api/schema/`
- Download the OpenAPI 3.0 schema
- Use with any OpenAPI-compatible tool

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register a new user | No |
| POST | `/api/auth/login/` | Login and get JWT tokens | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| GET | `/api/auth/me/` | Get current user info | Yes |
| PUT | `/api/auth/change-password/` | Change password | Yes |

### User Management Endpoints (Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/auth/users/` | List all users | Admin |
| GET | `/api/auth/users/{id}/` | Get user details | Admin |
| PATCH | `/api/auth/users/{id}/update_role/` | Update user role | Admin |

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | List all tasks (paginated) | Yes |
| GET | `/api/tasks/{id}/` | Get task details | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| PUT | `/api/tasks/{id}/` | Update a task | Yes |
| PATCH | `/api/tasks/{id}/` | Partially update a task | Yes |
| DELETE | `/api/tasks/{id}/` | Delete a task | Yes |

### Additional Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/completed/` | List completed tasks | Yes |
| GET | `/api/tasks/incomplete/` | List incomplete tasks | Yes |
| POST | `/api/tasks/{id}/mark_complete/` | Mark task as complete | Yes |
| POST | `/api/tasks/{id}/mark_incomplete/` | Mark task as incomplete | Yes |

### Query Parameters for Task List

- **Filtering**:
  - `?completed=true` - Filter completed tasks
  - `?completed=false` - Filter incomplete tasks
  - `?created_after=2024-01-01` - Filter tasks created after date
  - `?created_before=2024-12-31` - Filter tasks created before date
  - `?title=search` - Filter by title (case-insensitive)

- **Search**:
  - `?search=keyword` - Search in title and description

- **Ordering**:
  - `?ordering=created_at` - Order by creation date (ascending)
  - `?ordering=-created_at` - Order by creation date (descending)
  - `?ordering=title` - Order by title
  - `?ordering=completed` - Order by completion status

- **Pagination**:
  - `?page=2` - Get page 2
  - Default page size: 10 items

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication.

### Getting Access Tokens

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "password": "securepass123",
       "password2": "securepass123",
       "first_name": "John",
       "last_name": "Doe"
     }'
   ```

2. **Login to get tokens**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "password": "securepass123"
     }'
   ```

   Response:
   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   ```

3. **Use the access token in requests**:
   ```bash
   curl -X GET http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

4. **Refresh the access token** (when it expires):
   ```bash
   curl -X POST http://localhost:8000/api/auth/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
   ```

### Token Lifetimes

- **Access Token**: 60 minutes
- **Refresh Token**: 1 day

## 👥 User Roles

The API implements role-based access control with two roles:

### Regular User
- Can create, read, update, and delete their own tasks
- Can view only their own tasks
- Can update their own profile
- Cannot access admin endpoints

### Admin User
- Can view all tasks from all users
- Can update and delete any task
- Can list all users
- Can update user roles
- Has all Regular User permissions

### Setting User Roles

User roles can only be changed by admin users through the admin panel or API:

```bash
curl -X PATCH http://localhost:8000/api/auth/users/{user_id}/update_role/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "ADMIN"}'
```

## 💡 Usage Examples

### Example 1: Register and Create a Task

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "taskmaster",
    "email": "task@example.com",
    "password": "secure123",
    "password2": "secure123"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "taskmaster",
    "password": "secure123"
  }'

# Save the access token from response

# 3. Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Project Documentation",
    "description": "Write comprehensive README and API docs",
    "completed": false
  }'
```

### Example 2: Get Filtered Tasks

```bash
# Get all incomplete tasks
curl -X GET "http://localhost:8000/api/tasks/?completed=false" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Search tasks
curl -X GET "http://localhost:8000/api/tasks/?search=documentation" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get tasks with pagination
curl -X GET "http://localhost:8000/api/tasks/?page=2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Example 3: Update a Task

```bash
# Partially update a task (mark as complete)
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Or use the convenience endpoint
curl -X POST http://localhost:8000/api/tasks/1/mark_complete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Example 4: Python Requests Library

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Register
register_data = {
    "username": "pythonuser",
    "email": "python@example.com",
    "password": "pythonpass123",
    "password2": "pythonpass123"
}
response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
print(response.json())

# Login
login_data = {
    "username": "pythonuser",
    "password": "pythonpass123"
}
response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
tokens = response.json()
access_token = tokens['access']

# Set headers with token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Create a task
task_data = {
    "title": "Learn Django REST Framework",
    "description": "Build a complete API with authentication",
    "completed": False
}
response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
tasks = response.json()
print(f"Found {tasks['count']} tasks")

# Update a task
task_id = 1
update_data = {"completed": True}
response = requests.patch(f"{BASE_URL}/tasks/{task_id}/", json=update_data, headers=headers)
print(response.json())
```

## 📝 Request/Response Examples

### Create Task Request
```json
POST /api/tasks/
{
  "title": "Complete API Documentation",
  "description": "Write comprehensive docs with examples",
  "completed": false
}
```

### Create Task Response
```json
{
  "id": 1,
  "title": "Complete API Documentation",
  "description": "Write comprehensive docs with examples",
  "completed": false,
  "created_at": "2024-10-17T10:30:00Z",
  "updated_at": "2024-10-17T10:30:00Z",
  "user": "johndoe"
}
```

### List Tasks Response
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Task 1",
      "description": "Description 1",
      "completed": false,
      "created_at": "2024-10-17T10:30:00Z",
      "updated_at": "2024-10-17T10:30:00Z",
      "user": "johndoe"
    },
    ...
  ]
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

### Database Configuration

The project uses SQLite by default. To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contributing

This is a project created for an assignment. However, suggestions and improvements are welcome!

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created as part of a Django REST Framework assignment.

## 📞 Support

For questions or issues:
- Check the API documentation at `/api/docs/`
- Review the test cases for usage examples
- Refer to Django REST Framework documentation

## 🎯 Assignment Requirements Checklist

### Core Requirements
- ✅ Task Model with all required fields (id, title, description, completed, created_at, updated_at)
- ✅ All CRUD endpoints implemented (GET, POST, PUT, DELETE)
- ✅ JWT authentication implemented
- ✅ User registration and login
- ✅ Only authenticated users can create/update/delete tasks
- ✅ API documentation (Swagger and ReDoc)
- ✅ Unit tests with instructions

### Bonus Features
- ✅ Pagination implemented
- ✅ Filtering by completed status
- ✅ Additional filters (date range, title search)
- ✅ User roles (Admin and Regular User)
- ✅ Role-based permissions
- ✅ Comprehensive test coverage (43 tests)

## 🚀 Quick Start Cheat Sheet

```bash
# Setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Test
python manage.py test
coverage run --source='.' manage.py test
coverage report

# Access
# API: http://localhost:8000/api/
# Docs: http://localhost:8000/api/docs/
# Admin: http://localhost:8000/admin/
```

---

**Happy Task Managing! 🎉**

