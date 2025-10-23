from __future__ import annotations
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.conf import settings
from openai import OpenAI
from .models import TrendItem


@login_required
def feed(request):
    business_type = request.GET.get("type", "spa")
    items = TrendItem.objects.filter(business_type=business_type).order_by("-created_at")[:20]
    if not items:
        # generate sample via AI or fallback
        lang = get_language() or "en"
        suggestions = generate_trends(business_type, lang)
        for s in suggestions:
            TrendItem.objects.create(business_type=business_type, title=s, description="")
        items = TrendItem.objects.filter(business_type=business_type).order_by("-created_at")[:20]
    return render(request, "trends/feed.html", {"items": items, "business_type": business_type})


def generate_trends(business_type: str, language: str) -> list[str]:
    if not settings.OPENAI_API_KEY:
        return [
            "HydraFacial + LED combo",
            "Scalp detox therapy",
            "Retinol + peptide evening routine",
        ]
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system = "You curate global beauty treatment trends and innovations."
    user = f"Language: {language}. Top 5 current trending treatments for a {business_type}. Return a bullet list."
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.6,
        )
        content = completion.choices[0].message.content or ""
        lines = [l.strip("- • ") for l in content.splitlines() if l.strip()]
        return [l for l in lines if l]
    except Exception:
        return ["Vitamin C facial", "Microneedling", "Keratin hair treatment"]
