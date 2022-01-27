from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from .models import CustomUser as User


class IsSelfOrReadOnly(BasePermission):
    message = "can't edit/delete another user, only yourself"

    def has_object_permission(self, request: Request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj


class IsAdmin(BasePermission):
    message = "only for admins"

    def has_permission(self, request: Request, view):
        return type(request.user) is User and request.user.is_stuff

    def has_object_permission(self, request: Request, view, obj):
        return self.has_permission(request, view)


class IfObjAdminReadOnly(BasePermission):
    message = "can't edit/delete admin users"

    def has_object_permission(self, request: Request, view, obj):
        return (
            request.method in SAFE_METHODS or type(obj) is not User or not obj.is_stuff
        )


class Any(BasePermission):
    pass
