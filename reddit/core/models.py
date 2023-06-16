from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class M2mUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Subreddit(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    subs = models.ForeignKey(M2mUser, null=True, blank=True, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    votes = models.ForeignKey(M2mUser, null=True, blank=True, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    votes = models.ForeignKey(M2mUser, null=True, blank=True, on_delete=models.CASCADE)
