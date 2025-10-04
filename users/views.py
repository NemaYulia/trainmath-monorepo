from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from core.models import Attempt
from django.db.models import Avg, Count, Q


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматичний вхід після реєстрації
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def profile_view(request):
    user = request.user
    attempts = Attempt.objects.filter(user=user)

    # Базова статистика
    total = attempts.count()
    correct = attempts.filter(is_correct=True).count()
    accuracy = (correct / total * 100) if total > 0 else 0
    avg_time = attempts.aggregate(Avg("time_taken_ms"))["time_taken_ms__avg"]

    return render(request, "users/profile.html", {
        "user": user,
        "attempts": attempts.order_by("-created_at")[:10],
        "accuracy": round(accuracy, 2),
        "avg_time": round(avg_time, 2) if avg_time else None,
        "total": total,
    })

