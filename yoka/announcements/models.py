from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext as _

User = get_user_model()


class AnnouncementQueryset(models.QuerySet):

    def visible(self):
        return self.filter(release_date__lte=timezone.now())


class Announcement(models.Model):
    """お知らせ用モデル"""
    title = models.CharField(_("タイトル"), max_length=100)
    content = models.TextField(_("内容"), max_length=3000)
    release_date = models.DateTimeField(_("公開日時"), default=timezone.now)
    update_date = models.DateTimeField(_("更新日時"), auto_now=True)
    update_user = models.ForeignKey(
        User, verbose_name=_("更新者"), on_delete=models.SET_NULL, null=True, related_name="update_info",
    )
    create_date = models.DateTimeField(_("作成日時"), default=timezone.now)
    create_user = models.ForeignKey(
        User, verbose_name=_("作成者"), on_delete=models.SET_NULL, null=True, related_name="create_info",
    )

    objects = AnnouncementQueryset.as_manager()

    class Meta:
        ordering = ["-release_date"]
        verbose_name = _("お知らせ")
        verbose_name_plural = _("お知らせ")

    def __str__(self):
        return self.title
