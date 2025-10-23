from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from openai import OpenAI
from .models import TreatmentPlan


@login_required
def form(request):
    if request.method == "POST":
        skin_type = request.POST.get("skin_type", "")
        hair_type = request.POST.get("hair_type", "")
        age = int(request.POST.get("age") or 0)
        previous = request.POST.get("previous", "")
        client_name = request.POST.get("client_name", "")
        lang = get_language() or "en"

        suggestion = generate_plan(skin_type, hair_type, age, previous, lang)
        TreatmentPlan.objects.create(
            created_by=request.user,
            client_name=client_name,
            skin_type=skin_type,
            hair_type=hair_type,
            age=age,
            previous_treatments=previous,
            suggested_plan=suggestion,
            language=lang,
        )
        messages.success(request, "Plan saved to history.")
        return redirect("planner:list")

    return render(request, "planner/form.html")


@login_required
def list_plans(request):
    plans = TreatmentPlan.objects.filter(created_by=request.user)[:50]
    return render(request, "planner/list.html", {"plans": plans})


def generate_plan(skin_type: str, hair_type: str, age: int, previous: str, language: str) -> str:
    if not settings.OPENAI_API_KEY:
        # Fallback sample
        return (
            f"Personalized plan for age {age}, skin {skin_type}, hair {hair_type}. "
            f"Consider hydration, SPF50 daily, gentle retinol 2-3x/week. Professional facials monthly."
        )
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system = (
        "You are an expert beauty and aesthetics consultant. Produce safe, practical, step-by-step treatment plans "
        "for clinics/spas/salons. Include at-home routine and in-clinic suggestions, with clear cautions."
    )
    user = (
        f"Language: {language}. Client age: {age}. Skin type: {skin_type}. Hair type: {hair_type}. "
        f"Previous treatments: {previous}. Output concise numbered steps and schedule."
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.7,
        )
        return completion.choices[0].message.content or ""
    except Exception:
        return (
            "AI temporarily unavailable. Suggested basics: daily SPF, gentle cleanser, moisturizer, and periodic professional care."
        )
