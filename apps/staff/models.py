from __future__ import annotations
from django.db import models
from django.conf import settings


class StaffMember(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, blank=True)
    shift = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
