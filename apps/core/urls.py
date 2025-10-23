from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("setup/", views.setup_wizard, name="setup"),
]
