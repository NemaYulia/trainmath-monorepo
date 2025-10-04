# core/models.py
from django.db import models
from django.conf import settings
import uuid

class ProblemType(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    impl_path = models.CharField(max_length=300, help_text="dotted path to problem class")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProblemInstance(models.Model):
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(choices=[(1,'easy'),(2,'medium'),(3,'hard')])
    params = models.JSONField()
    question_text = models.TextField()
    canonical_answer = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=128, null=True, blank=True)  # for guests
    problem = models.ForeignKey(ProblemInstance, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    time_taken_ms = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ShareResult(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
