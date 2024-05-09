from typing import Iterable
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from app.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_reviewer = models.BooleanField(
        _("reviewer"), default=False, help_text=_("Can review hotels")
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
