from .base import *

DEBUG = True

ALLOWED_HOSTS = ("localhost",)

CORS_ALLOWED_ORIGINS = ["http://localhost:1337"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337"]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", os.getenv("DB_USER")),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
