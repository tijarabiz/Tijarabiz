from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("features/", views.features, name="features"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contact, name="contact"),
    path("pricing/", views.pricing, name="pricing"),
    path("signup/", views.signup, name="signup"),
    path("subscribe/checkout/", views.create_checkout_session, name="checkout"),
    path("subscribe/success/", views.subscribe_success, name="subscribe_success"),
    path("subscribe/cancel/", views.subscribe_cancel, name="subscribe_cancel"),
]