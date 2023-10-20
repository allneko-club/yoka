from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yoka.users"
    verbose_name = _("ユーザー")

    def ready(self):
        try:
            import yoka.users.signals  # noqa F401
        except ImportError:
            pass
