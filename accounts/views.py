from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer
)
from .models import UserProfile
from tasks.permissions import IsAdminUser


@extend_schema_view(
    post=extend_schema(
        description='Register a new user account',
        summary='Register user',
        request=UserRegistrationSerializer,
        responses={201: UserSerializer}
    )
)
class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serializer = UserSerializer(user)
        return Response(
            {
                'user': user_serializer.data,
                'message': 'User registered successfully'
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    description='Get current user profile information',
    summary='Get user profile',
    responses={200: UserSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get the current authenticated user's information.
    
    GET /api/auth/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    description='Change the current user\'s password',
    summary='Change password',
    request=ChangePasswordSerializer,
    responses={200: {'description': 'Password changed successfully'}}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change password for the current user.
    
    PUT /api/auth/change-password/
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not user.check_password(serializer.data.get('old_password')):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        description='List all users (Admin only)',
        summary='List users'
    ),
    retrieve=extend_schema(
        description='Get user details by ID (Admin only)',
        summary='Get user details'
    ),
    update=extend_schema(
        description='Update user role (Admin only)',
        summary='Update user'
    ),
    partial_update=extend_schema(
        description='Partially update user role (Admin only)',
        summary='Partially update user'
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management (Admin only).
    
    Allows admins to:
    - List all users
    - View user details
    - Update user roles
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['get', 'put', 'patch']  # No delete or create
    
    @extend_schema(
        description='Update user role (Admin only)',
        summary='Update user role',
        request=UserProfileSerializer
    )
    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        """Update a user's role (Admin only)"""
        user = self.get_object()
        profile = user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
