from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yoka.notifications"
    verbose_name = _("通知")

    def ready(self):
        try:
            import yoka.notifications.signals  # noqa
        except ImportError:
            pass
