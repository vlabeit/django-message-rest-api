from rest_framework import permissions

class BaseUserPermission(permissions.BasePermission):
    """Base permission for user actions"""
    def has_permission(self, request, view):
        """Check permissions for the list and create action"""
        allowed_actions = ['list', 'retrieve', 'update', 'partial_update'] #'create'
        return request.user.is_authenticated if view.action in allowed_actions else True

class UpdateUserPermission(BaseUserPermission):
    """Allow users to edit own user data"""
    def has_object_permission(self, request, view, obj):
        """Check the user updating data"""
        return request.user.is_authenticated and obj.id == request.user.id

class ViewMessagePermission(BaseUserPermission):
    def has_permission(self, request, view):
        """Check permissions for the list and create action"""
        allowed_actions = ['list', 'retrieve', 'update', 'partial_update', 'create']
        return request.user.is_authenticated if view.action in allowed_actions else True
    """Allow users to view, edit, delete own user data"""
    def has_object_permission(self, request, view, obj):
        """Check the user updating data"""
        return request.user.is_authenticated and (
            obj.message_from == request.user or obj.message_to == request.user
        )