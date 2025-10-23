from __future__ import annotations
from django.db import models
from django.conf import settings


class Client(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
