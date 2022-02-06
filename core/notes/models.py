from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Note(models.Model):
    BY_URL = "BU"
    PRIVATE = "PR"
    VISIBILITY_CHOICES = [
        (BY_URL, "by url"),
        (PRIVATE, "private"),
    ]
    id = models.UUIDField(
        primary_key=True, editable=False, auto_created=True, default=uuid4
    )
    text = models.CharField(max_length=500)
    visibility = models.CharField(
        max_length=2, choices=VISIBILITY_CHOICES, default=PRIVATE
    )
    author = models.ForeignKey(User, models.CASCADE, related_name="notes")
    creation_date = models.DateTimeField("created date", auto_now=True, editable=False)

    def __str__(self):
        return self.text
