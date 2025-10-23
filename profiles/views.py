from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Count

from .models import Application
from accounts.models import Profile

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
    term = request.GET.get('q', '').strip()

    qs = Profile.objects.select_related('user').filter(privacy='public')

    if term:
        qs = qs.filter(
            Q(user__username__icontains=term) |
            Q(headline__icontains=term) |
            Q(skills__icontains=term) |
            Q(education__icontains=term) |
            Q(work_experience__icontains=term)
        )

    return render(request, 'candidate_search.html', {'candidates': qs})
