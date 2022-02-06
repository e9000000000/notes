from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsAuthorOrReadOnlyIfNotPrivate(BasePermission):
    message = (
        "only author can edit/delete. no authors can only read if it's not private."
    )

    def has_object_permission(self, request, view, obj):
        return (obj.visibility == obj.BY_URL and request.method in SAFE_METHODS) or (
            type(request.user) is User and obj.author == request.user
        )
