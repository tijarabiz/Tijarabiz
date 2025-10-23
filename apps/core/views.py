from __future__ import annotations
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from .models import Business, Subscription


def require_active_or_trial(view_func):
    def _wrapped(request, *args, **kwargs):
        membership = getattr(request.user, "businessmembership_set", None)
        business = None
        if membership:
            membership_obj = membership.first()
            if membership_obj:
                business = membership_obj.business
        if not business:
            messages.info(request, _("Please complete setup to create your business."))
            return redirect("core:setup")
        # Gate access
        subscription = getattr(business, "subscription", None)
        if subscription and subscription.is_active:
            return view_func(request, *args, **kwargs)
        if business.on_trial:
            return view_func(request, *args, **kwargs)
        messages.warning(request, _("Your trial has ended. Please subscribe."))
        return redirect("website:pricing")

    return _wrapped


@login_required
@require_active_or_trial
def dashboard(request):
    return render(request, "core/dashboard.html", {})


@login_required
def setup_wizard(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        business_type = request.POST.get("business_type")
        num_staff = int(request.POST.get("num_staff") or 1)
        # One trial per unique name and email
        if Business.objects.filter(name=name).exists() or Business.objects.filter(email=email).exists():
            messages.error(request, _("A trial already exists for this business name or email."))
            return redirect("core:setup")
        business = Business.start_trial(
            owner=request.user,
            name=name,
            email=email,
            phone=phone or "",
            business_type=business_type or "spa",
            num_staff=num_staff,
        )
        Subscription.objects.create(business=business, is_active=False)
        messages.success(request, _("Trial started! Enjoy 30 days of full access."))
        return redirect("core:dashboard")

    return render(request, "core/setup.html", {})
