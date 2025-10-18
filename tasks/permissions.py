from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a task or admins to edit/delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to authenticated users
        if request.method in permissions.SAFE_METHODS:
            # Allow if user is admin or owner
            if hasattr(request.user, 'profile') and request.user.profile.is_admin():
                return True
            return obj.user == request.user
        
        # Write permissions are only allowed to the owner or admin
        if hasattr(request.user, 'profile') and request.user.profile.is_admin():
            return True
        return obj.user == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.is_admin()
        )

