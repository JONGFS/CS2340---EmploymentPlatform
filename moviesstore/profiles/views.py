from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Count

from .models import Application, CandidateProfile

@login_required
def my_applications(request):
    apps = (
        Application.objects
        .select_related("job")
        .filter(candidate=request.user)
        .order_by("-updated_at")
    )
    return render(request, "my_applications.html", {"apps": apps})

def candidate_search(request):
    q = (request.GET.get("q") or "").strip()
    candidates = (
        CandidateProfile.objects
        .select_related("user")
        .prefetch_related("work_experience")
        .all()
    )
    if q:
        candidates = candidates.filter(
            Q(user__username__icontains=q) |
            Q(headline__icontains=q) |
            Q(location__icontains=q) |
            Q(education__icontains=q) |
            Q(skills__icontains=q)
        )

    return render(
        request,
        "candidate_search.html",
        {"candidates": candidates, "q": q},
    )
