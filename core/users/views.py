from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    UserSerializer,
    ChangeUserPasswordSerializer,
    RegistrationSerializer,
)


User = get_user_model()


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []

    @extend_schema(
        tags=["user"],
        summary="register new user",
        description="register new user with username and password. \
            user should solve captcha to be registered.",
        responses={
            204: OpenApiResponse(description="registration success"),
            400: OpenApiResponse(
                description="wrong request data",
            ),  # TODO: make response body for 400 error
        },
    )
    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=204)


class SelfViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        raise NotImplementedError("can't get multiple objects")

    @extend_schema(
        tags=["user"],
        summary="get self data",
        description="get data of authenticated user",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(  # TODO: make detailed error response
                description="not authenticated",
            ),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @extend_schema(
        tags=["user"],
        summary="delete self",
        description="delete account of authenticated user",
        responses={
            204: OpenApiResponse(description="success"),
            401: OpenApiResponse(
                description="not authenticated"
            ),  # TODO: add response body {detail: error detail}
        },
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    @extend_schema(
        tags=["user"],
        summary="update self",
        description="update data of authenticated user",
        responses={
            200: UserSerializer,
            400: OpenApiResponse(
                description="invalid data"
            ),  # TODO: add response body {detail: error detail}
            401: OpenApiResponse(
                description="not authenticated"
            ),  # TODO: add response body {detail: error detail}
        },
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)


class AuthView(ObtainAuthToken):
    authentication_classes = []

    @extend_schema(
        tags=["user"],
        summary="authenticate",
        description="get authentication token",
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class UnAuthView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["user"],
        summary="delete auth token",
        responses={
            204: OpenApiResponse(description="success"),
            403: OpenApiResponse(  # TODO: make normal docs for error responses
                description="should be authenticated",
            ),
            404: OpenApiResponse(description="no tokens found"),
        },
    )
    def delete(self, request: Request, format=None):
        user = request.user
        try:
            token = Token.objects.get(user=user.pk)
            token.delete()
        except Token.DoesNotExist:
            raise NotFound(
                f"user have no token {user.username=}, so how you made it authenticated?!"
            )

        return Response(status=204)


class ChangePasswordView(APIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["user"],
        summary="change user password",
        responses={
            204: OpenApiResponse(description="success"),
            400: OpenApiResponse(description="invalid old password"),
            401: OpenApiResponse(description="not authenticated"),
        },
    )
    def patch(self, request: Request, format=None):
        """change user password"""

        serializer = self.serializer_class(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.auth.delete()
        return Response(status=204)
