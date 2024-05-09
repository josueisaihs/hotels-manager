import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.getenv("DJANGO_ENV", "local")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"app.config.settings.{DJANGO_ENV}")


app = Celery("tasks")

# Use synchronous task execution
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=False,
)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f"Celery works!"
