from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator


class CustomUser(AbstractBaseUser):
    """
    custom user model
    username and password fields are required, other - optional
    """

    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        "username",
        max_length=36,
        unique=True,
        help_text="required. 36 characters or fewer. only ascii symbols.",
        validators=[username_validator],
        error_messages={
            "unique": "a user with that username already exists.",
        },
    )
    registration_date = models.DateTimeField(
        "registration date", auto_now=True, editable=False
    )

    USERNAME_FIELD = "username"
    objects = UserManager()
