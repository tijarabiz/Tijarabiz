from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("kpis/", views.kpis, name="kpis"),
]