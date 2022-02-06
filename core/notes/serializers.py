from rest_framework.serializers import ModelSerializer

from .models import Note


class NotesSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "text", "visibility", "author", "creation_date"]
        read_only_fields = ["id", "creation_date", "author"]
