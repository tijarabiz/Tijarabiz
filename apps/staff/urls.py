from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path("", views.list_staff, name="list"),
]