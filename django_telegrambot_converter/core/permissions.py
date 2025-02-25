from rest_framework.permissions import BasePermission


class IsRaman(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.username == 'raman'