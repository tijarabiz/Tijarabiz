from __future__ import annotations
from django.db import models
from django.conf import settings
from django.utils import timezone


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    stock = models.PositiveIntegerField(default=0)
    expires_at = models.DateField(null=True, blank=True)

    def is_expiring_soon(self) -> bool:
        if not self.expires_at:
            return False
        return self.expires_at <= timezone.now().date()
