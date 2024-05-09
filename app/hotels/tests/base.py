import os
from pathlib import Path

from django.contrib.auth import get_user_model


User = get_user_model()

image_path = os.path.join(Path(__file__).parent.resolve(), "fixtures", "test.png")

TEST_LOCATION = [
    ("madrid", "Madrid"),
    ("barcelona", "Barcelona"),
]

simple_msg = lambda expected, result: f"Expected {expected} but got {result}"


def ignore_fields(data: dict, fields: list) -> dict:
    for field in fields:
        data.pop(field, None)
    return data
