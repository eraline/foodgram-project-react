from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
        blank=False
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username
