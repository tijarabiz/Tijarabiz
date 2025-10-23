from django.urls import path
from . import views

app_name = "trends"

urlpatterns = [
    path("", views.feed, name="feed"),
]