from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext as _
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY or None


def home(request):
    return render(request, "website/home.html")


def about(request):
    return render(request, "website/about.html")


def features(request):
    return render(request, "website/features.html")


def blog(request):
    return render(request, "website/blog.html")


def contact(request):
    return render(request, "website/contact.html")


def pricing(request):
    return render(request, "website/pricing.html")


def signup(request):
    # Two options: Free Trial (no payment) -> dashboard setup, or Paid Subscription/Coupon
    if request.method == "POST":
        action = request.POST.get("action")  # free_trial or paid
        if action == "free_trial":
            # Create user account
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, _("Welcome! Start your setup."))
                return redirect("core:setup")
            else:
                messages.error(request, _("Please correct the errors below."))
        elif action == "paid":
            # Require login/create first, then redirect to checkout with coupon if provided
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("website:checkout")
            else:
                messages.error(request, _("Please correct the errors below."))
    else:
        form = UserCreationForm()
    return render(request, "website/signup.html", {"form": form})


def create_checkout_session(request):
    if not stripe.api_key:
        messages.error(request, _("Payments are not configured."))
        return redirect("website:pricing")
    coupon_code = request.GET.get("coupon")

    discounts = []
    if coupon_code:
        try:
            coupon = stripe.Coupon.retrieve(coupon_code)
            discounts = [{"coupon": coupon["id"]}]
        except Exception:
            discounts = []

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            allow_promotion_codes=True,
            discounts=discounts or None,
            success_url=f"http://{settings.SITE_DOMAIN}/subscribe/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://{settings.SITE_DOMAIN}/subscribe/cancel/",
        )
        return redirect(session.url)
    except Exception as exc:  # pragma: no cover
        messages.error(request, str(exc))
        return redirect("website:pricing")


def subscribe_success(request):
    messages.success(request, _("Subscription activated!"))
    return redirect("core:dashboard")


def subscribe_cancel(request):
    messages.info(request, _("Subscription canceled."))
    return redirect("website:pricing")
