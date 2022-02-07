from django.contrib.auth.models import AbstractUser
from django.db import models
import enum


class Roles(str, enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    role = models.CharField(
        'Роль',
        blank=False,
        max_length=20,
        choices=ROLES, default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        'E-mail',
        blank=False,
        unique=True,
    )

    class Meta:
        ordering = ('username',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique user'
            ),
        )

    @property
    def is_administrator(self):
        return self.role == Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR
