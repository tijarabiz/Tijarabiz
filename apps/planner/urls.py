from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.form, name="form"),
    path("list/", views.list_plans, name="list"),
]
