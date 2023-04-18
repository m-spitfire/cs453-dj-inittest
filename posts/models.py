from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Post model."""

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
