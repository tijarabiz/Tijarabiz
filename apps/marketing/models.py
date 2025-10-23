from __future__ import annotations
from django.db import models
from django.conf import settings


class Campaign(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    channel = models.CharField(max_length=50, default="social")
    created_at = models.DateTimeField(auto_now_add=True)
