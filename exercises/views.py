
from django.db.models import Avg, Count, Q
from core.models import Attempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def exercises_home(request):
    return render(request, "exercises/home.html")
@login_required
def stats_view(request):
    attempts = Attempt.objects.filter(user=request.user)

    by_type = attempts.values(
        "problem__problem_type__name",
        "problem__difficulty"
    ).annotate(
        total=Count("id"),
        correct=Count("id", filter=Q(is_correct=True)),
        avg_time=Avg("time_taken_ms")
    )

    return render(request, "exercises/stats.html", {"by_type": by_type})
