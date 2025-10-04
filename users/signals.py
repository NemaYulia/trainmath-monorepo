# users/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from core.models import Attempt

@receiver(user_logged_in)
def move_guest_attempts(sender, request, user, **kwargs):
    session_id = request.session.session_key
    if session_id:
        Attempt.objects.filter(session_id=session_id, user__isnull=True).update(
            user=user,
            session_id=None
        )
