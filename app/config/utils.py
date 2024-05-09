from uuid import uuid4
from typing import Union

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def photo_directory_path(instance: models.Model, filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    ext = filename.split(".")[-1]
    folder = slugify(instance._meta.verbose_name_plural)  # type: ignore

    return f"{folder}/{uuid4()}.{ext}"
