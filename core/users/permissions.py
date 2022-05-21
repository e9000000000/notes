from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsSelf(BasePermission):
    message = "can't access another user data"

    def has_object_permission(self, request: Request, view, obj):
        return request.user == obj


class Any(BasePermission):
    pass
