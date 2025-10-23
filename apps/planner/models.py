from __future__ import annotations
from django.db import models
from django.conf import settings
from django.utils import timezone


class TreatmentPlan(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, blank=True)
    skin_type = models.CharField(max_length=100, blank=True)
    hair_type = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(default=0)
    previous_treatments = models.TextField(blank=True)
    suggested_plan = models.TextField()
    language = models.CharField(max_length=10, default="en")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
