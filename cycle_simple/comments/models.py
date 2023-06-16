from django.db import models


class Comment(models.Model):
    content = models.TextField()
    reply_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
