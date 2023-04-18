from .base import *  # noqa
from .base import env

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-secret",
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

INSTALLED_APPS += ["drf_spectacular"]  # noqa: F405

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
}

CORS_ORIGIN_ALLOW_ALL = True
