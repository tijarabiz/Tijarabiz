from __future__ import annotations
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.conf import settings
from openai import OpenAI
from .models import Campaign


@login_required
def generate(request):
    generated = None
    if request.method == "POST":
        topic = request.POST.get("topic", "New treatment promotion")
        lang = get_language() or "en"
        generated = generate_campaign(topic, lang)
        Campaign.objects.create(owner=request.user, title=topic, content=generated)
    return render(request, "marketing/generate.html", {"generated": generated})


def generate_campaign(topic: str, language: str) -> str:
    if not settings.OPENAI_API_KEY:
        return f"Campaign idea for {topic}: Offer 20% off this week."
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system = "You are a marketing copy expert for beauty businesses."
    user = f"Language: {language}. Create a short social post and email copy for: {topic}."
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.7,
        )
        return completion.choices[0].message.content or ""
    except Exception:
        return "Short promo: Book now and save 20%!"
