from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound, NotAuthenticated, ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .permissions import IsSelf, Any
from .serializers import (
    UserSerializer,
    ChangeUserPasswordSerializer,
    RegistrationSerializer,
)


User = get_user_model()


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [Any]

    @extend_schema(
        tags=["registration"],
        summary="register new user",
        description="register new user with username and password. \
            user should solve captcha to be registered.",
        responses={
            200: OpenApiResponse(description="registration success"),
            400: OpenApiResponse(
                description="wrong request data",
            ),  # TODO: make response body for 400 error
        },
    )
    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response()


class SelfViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        raise NotImplementedError("can't get multiple objects")

    @extend_schema(
        tags=["self"],
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
        tags=["self"],
        summary="delete self",
        description="delete account of authenticated user",
        responses={
            200: OpenApiResponse(
                description="success"
            ),  # TODO: ckeck, may be 201 or 202 or something like that
            401: OpenApiResponse(
                description="not authenticated"
            ),  # TODO: add response body {detail: error detail}
        },
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)

    @extend_schema(
        tags=["self"],
        summary="update self",
        description="update data of authenticated user",
        responses=UserSerializer,
        # responses={
        #     200: OpenApiResponse(
        #         description="success"
        #     ),  # TODO: ckeck, may be 201 or 202 or something like that
        #     400: OpenApiResponse(
        #         description="invalid data"
        #     ),  # TODO: add response body {detail: error detail}
        #     401: OpenApiResponse(
        #         description="not authenticated"
        #     ),  # TODO: add response body {detail: error detail}
        # },
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)


class Auth(ObtainAuthToken):
    @extend_schema(
        tags=["auth"],
        summary="authenticate",
        description="get authentication token",
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    @extend_schema(
        tags=["auth"],
        summary="delete auth token",
        description="make token unuseable",
        responses={
            200: OpenApiResponse(description="success"),
            403: OpenApiResponse(  # TODO: make normal docs for error responses
                description="should be authenticated",
            ),
            404: OpenApiResponse(description="no tokens found"),
        },
    )
    def delete(self, request: Request, format=None):
        """delete auth token"""

        if type(request.user) is not User:
            raise NotAuthenticated("not authenticated")
        user = request.user
        try:
            token = Token.objects.get(user=user.pk)
            token.delete()
        except Token.DoesNotExist:
            raise NotFound(f"user have no token {user.username=}")

        return Response()


class ChangePasswordView(APIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["self"],
        summary="change user password",
        responses={
            200: OpenApiResponse(description="success"),
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
        return Response()
