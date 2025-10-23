from __future__ import annotations
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def kpis(request):
    data = {
        "revenue": 0,
        "engagement": 0,
        "inventory_low": 0,
    }
    return JsonResponse(data)
