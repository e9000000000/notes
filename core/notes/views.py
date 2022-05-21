from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import NotesSerializer
from .models import Note
from .permissions import IsAuthorOrReadOnlyIfNotPrivate


class NotesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, format=None):
        """get your note list"""

        serializer = NotesSerializer(request.user.notes.all(), many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        """create new note"""

        data = request.data
        serializer = NotesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)


class NoteDetailsView(APIView):
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

    def get(self, request: Request, pk, format=None):
        """get note details"""

        serializer = NotesSerializer(self.get_object(request, pk))
        return Response(serializer.data)

    def patch(self, request: Request, pk, format=None):
        """update note details"""

        serializer = NotesSerializer(self.get_object(request, pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, pk, format=None):
        """delete note"""

        note = self.get_object(request, pk)
        note.delete()
        return Response({"success": 1})
