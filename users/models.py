from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
    )
