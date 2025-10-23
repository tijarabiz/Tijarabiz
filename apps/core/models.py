from __future__ import annotations
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Business(models.Model):
    BUSINESS_TYPES = [
        ("spa", "Spa"),
        ("salon", "Salon"),
        ("clinic", "Aesthetic Clinic"),
    ]

    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES)
    num_staff = models.PositiveIntegerField(default=1)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_businesses")

    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return self.name

    @property
    def on_trial(self) -> bool:
        if self.trial_end is None:
            return False
        return timezone.now() <= self.trial_end

    @classmethod
    def start_trial(cls, owner, name, email, phone, business_type, num_staff) -> "Business":
        now = timezone.now()
        trial_end = now + timedelta(days=30)
        return cls.objects.create(
            owner=owner,
            name=name,
            email=email,
            phone=phone,
            business_type=business_type,
            num_staff=num_staff,
            trial_start=now,
            trial_end=trial_end,
        )


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent_off = models.PositiveIntegerField(default=0)  # 0..100
    active = models.BooleanField(default=True)
    notes = models.CharField(max_length=255, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def is_valid(self) -> bool:
        now = timezone.now()
        if not self.active:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_to and now > self.valid_to:
            return False
        return True


class Subscription(models.Model):
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name="subscription")
    is_active = models.BooleanField(default=False)
    price_cents = models.IntegerField(default=10000)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def activate(self, coupon: Coupon | None = None) -> None:
        self.is_active = True
        self.started_at = timezone.now()
        if coupon:
            self.coupon = coupon
        self.save()


class BusinessMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default="admin")

    class Meta:
        unique_together = ("user", "business")
