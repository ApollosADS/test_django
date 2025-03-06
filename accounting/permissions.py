from rest_framework.permissions import BasePermission

class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Comptable').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff