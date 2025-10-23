from __future__ import annotations
from django.db import models


class TrendItem(models.Model):
    business_type = models.CharField(max_length=20, default="spa")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
