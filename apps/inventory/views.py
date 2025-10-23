from __future__ import annotations
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product


@login_required
def list_products(request):
    products = Product.objects.filter(owner=request.user).order_by("name")
    return render(request, "inventory/list.html", {"products": products})
