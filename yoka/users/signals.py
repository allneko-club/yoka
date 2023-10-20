from django.contrib.auth.signals import user_logged_in
from django.dispatch import Signal, receiver

from .models import LoginHistory

deactivate_user = Signal()


@receiver(user_logged_in)
def create_login_history(sender, user, request, **kwargs):
    # テスト時はHTTP_USER_AGENTが存在しないため、get()で取得している
    LoginHistory.objects.create(
        user=user,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )
