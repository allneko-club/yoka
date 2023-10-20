from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContactsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yoka.contacts"
    verbose_name = _("問い合わせ")

    def ready(self):
        try:
            import yoka.contacts.signals  # noqa F401
        except ImportError:
            pass
