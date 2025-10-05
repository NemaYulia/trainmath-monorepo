from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Avg, Q
from .models import ProblemType, ProblemInstance, Attempt, ShareResult
from django.contrib.auth import get_user_model

@admin.register(ProblemType)
class ProblemTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    search_fields = ['name', 'slug']
    readonly_fields = ['created']

@admin.register(ProblemInstance)
class ProblemInstanceAdmin(admin.ModelAdmin):
    list_display = ['problem_type', 'difficulty', 'created']
    list_filter = ['problem_type', 'difficulty', 'created']
    search_fields = ['question_text']
    readonly_fields = ['created']

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'is_correct', 'time_taken_ms', 'timestamp']
    list_filter = ['is_correct', 'problem__problem_type', 'problem__difficulty', 'timestamp']
    search_fields = ['user__username', 'user_answer']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

@admin.register(ShareResult)
class ShareResultAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'attempt', 'public', 'created']
    list_filter = ['public', 'created']
    readonly_fields = ['uuid', 'created']

# Custom admin dashboard view
def admin_dashboard_view(request):
    # Get statistics
    total_users = Attempt.objects.values('user').distinct().count()
    total_attempts = Attempt.objects.count()
    correct_attempts = Attempt.objects.filter(is_correct=True).count()
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
    
    # Statistics by problem type
    stats_by_type = Attempt.objects.values(
        'problem__problem_type__name'
    ).annotate(
        total=Count('id'),
        correct=Count('id', filter=Q(is_correct=True)),
        avg_time=Avg('time_taken_ms')
    ).order_by('-total')
    
    # Statistics by difficulty
    stats_by_difficulty = Attempt.objects.values(
        'problem__difficulty'
    ).annotate(
        total=Count('id'),
        correct=Count('id', filter=Q(is_correct=True)),
        avg_time=Avg('time_taken_ms')
    ).order_by('problem__difficulty')
    
    # Recent attempts
    recent_attempts = Attempt.objects.select_related(
        'user', 'problem', 'problem__problem_type'
    ).order_by('-timestamp')[:10]

    # Per-user summary for registered users
    User = get_user_model()
    registered_users = User.objects.all()
    user_summaries = []
    for u in registered_users:
        qs = Attempt.objects.filter(user=u)
        total = qs.count()
        correct = qs.filter(is_correct=True).count()
        avg_time = qs.aggregate(Avg('time_taken_ms'))['time_taken_ms__avg'] or 0
        user_summaries.append({
            'user': u,
            'total': total,
            'correct': correct,
            'accuracy': round((correct/total*100) if total else 0, 2),
            'avg_time': round(avg_time, 0),
        })
    
    context = {
        'title': 'Admin Dashboard',
        'total_users': total_users,
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'accuracy': round(accuracy, 2),
        'stats_by_type': stats_by_type,
        'stats_by_difficulty': stats_by_difficulty,
        'recent_attempts': recent_attempts,
        'user_summaries': user_summaries,
    }
    
    return render(request, 'core/admin_dashboard.html', context)
