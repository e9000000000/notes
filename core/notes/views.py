from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.views import extend_schema
from drf_spectacular.openapi import OpenApiResponse

from .serializers import NotesSerializer
from .models import Note
from .permissions import IsAuthorOrReadOnlyIfNotPrivate


class NotesView(APIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["notes"],
        summary="get list of your notes",
        responses={
            200: NotesSerializer(many=True),
            401: OpenApiResponse(description="not athenticated"),  # TODO: response body
        },
    )
    def get(self, request: Request, format=None):
        serializer = self.serializer_class(request.user.notes.all(), many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["notes"],
        summary="create new note",
        responses={
            200: NotesSerializer,
            400: OpenApiResponse(description="invalid data"),  # TODO: response body
            401: OpenApiResponse(description="not athenticated"),  # TODO: response body
        },
    )
    def post(self, request: Request, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)


class NoteDetailsView(APIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthorOrReadOnlyIfNotPrivate]

    def get_object(self, request, pk: str, format=None) -> Note:
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist as e:
            raise NotFound(f"note not found {pk=}")

        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, note):
                self.permission_denied(
                    request,
                    message=getattr(permission, "message", None),
                )
        return note

    @extend_schema(
        tags=["notes"],
        summary="get note data",
        responses={
            200: NotesSerializer,
            401: OpenApiResponse(description="not athenticated"),  # TODO: response body
            404: OpenApiResponse(description="not found"),
        },
    )
    def get(self, request: Request, pk, format=None):
        serializer = self.serializer_class(self.get_object(request, pk))
        return Response(serializer.data)

    @extend_schema(
        tags=["notes"],
        summary="update note data",
        responses={
            200: NotesSerializer,
            400: OpenApiResponse(description="invalid data"),  # TODO: response body
            401: OpenApiResponse(description="not athenticated"),  # TODO: response body
            404: OpenApiResponse(description="not found"),
        },
    )
    def patch(self, request: Request, pk, format=None):
        serializer = NotesSerializer(self.get_object(request, pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=["notes"],
        summary="delete note",
        responses={
            204: OpenApiResponse(description="success"),
            401: OpenApiResponse(description="not athenticated"),  # TODO: response body
            404: OpenApiResponse(description="not found"),
        },
    )
    def delete(self, request: Request, pk, format=None):
        note = self.get_object(request, pk)
        note.delete()
        return Response(status=204)
