from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client
import csv
from io import TextIOWrapper


@login_required
def list_clients(request):
    clients = Client.objects.filter(owner=request.user).order_by("name")
    return render(request, "clients/list.html", {"clients": clients})


@login_required
def import_clients(request):
    if request.method == "POST" and request.FILES.get("file"):
        f = request.FILES["file"]
        wrapper = TextIOWrapper(f.file, encoding="utf-8")
        reader = csv.DictReader(wrapper)
        count = 0
        for row in reader:
            Client.objects.create(
                owner=request.user,
                name=row.get("name") or row.get("Name") or "Unnamed",
                email=row.get("email") or row.get("Email") or "",
                phone=row.get("phone") or row.get("Phone") or "",
                notes=row.get("notes") or row.get("Notes") or "",
            )
            count += 1
        messages.success(request, f"Imported {count} clients.")
        return redirect("clients:list")

    return render(request, "clients/import.html")
