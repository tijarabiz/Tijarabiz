from __future__ import annotations
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StaffMember


@login_required
def list_staff(request):
    staff = StaffMember.objects.filter(owner=request.user).order_by("name")
    return render(request, "staff/list.html", {"staff": staff})
