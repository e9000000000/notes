from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_captcha.serializers import RestCaptchaSerializer

from .permissions import IsSelfOrReadOnly, IsAdmin, Any, IfObjAdminReadOnly
from .serializers import UserSerializer, ChangeUserPasswordSerializer


User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [Any]

    def post(self, request: Request, format=None):
        """create user"""

        captcha_serializer = RestCaptchaSerializer(data=request.data)
        captcha_serializer.is_valid(raise_exception=True)

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

class SelfDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, format=None):
        """get info about self"""

        serializer = UserSerializer(request.user)
        return Response(serializer.data)



class UserDetails(APIView):
    permission_classes = [IsAdmin | IsSelfOrReadOnly, IfObjAdminReadOnly]

    def get_object(self, request, pk: int, format=None) -> User:
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            raise NotFound(f"user not found {pk=}")

        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, user):
                self.permission_denied(
                    request,
                    message=getattr(permission, "message", None),
                )
        return user

    def get(self, request: Request, pk: int, format=None):
        """get info about user"""

        serializer = UserSerializer(self.get_object(request, pk))
        return Response(serializer.data)

    def patch(self, request: Request, pk: int, format=None):
        """update user data, return updated data"""

        serializer = UserSerializer(
            self.get_object(request, pk), request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk: int, format=None):
        """delete user"""

        self.get_object(request, pk).delete()
        return Response({"success": 1})


class Auth(ObtainAuthToken):
    def delete(self, request: Request, format=None):
        """delete auth token"""

        if type(request.user) is not User:
            raise NotAuthenticated("not authenticated")
        user = request.user
        try:
            token = Token.objects.get(user=user.pk)
            token.delete()
        except Token.DoesNotExist as e:
            raise NotFound(f"user have no token {user.username=}")

        return Response({"success": 1})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, format=None):
        """change user password"""

        serializer = ChangeUserPasswordSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.auth.delete()
        return Response({"success": 1})
