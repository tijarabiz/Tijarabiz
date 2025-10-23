from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.list_clients, name="list"),
    path("import/", views.import_clients, name="import"),
]