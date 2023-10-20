from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class ContactStatus(models.Model):
    """問い合わせステータスモデル"""
    name = models.CharField(_("ステータス名"), max_length=20, unique=True)
    rank = models.PositiveIntegerField(_("表示順"), unique=True)

    class Meta:
        ordering = ["rank"]
        verbose_name = _("問い合わせステータス")
        verbose_name_plural = _("問い合わせステータス")

    def __str__(self):
        return self.name


class Contact(models.Model):
    """問い合わせモデル"""
    email = models.EmailField(_("メールアドレス"))
    subject = models.CharField(
        _("タイトル"),
        max_length=50,
        help_text=_("50文字以内で入力して下さい。"),
    )
    message = models.TextField(
        _("本文"),
        max_length=1000,
        help_text=_("1000文字以内で入力して下さい。"),
    )
    status = models.ForeignKey(
        ContactStatus, verbose_name=_("ステータス"), on_delete=models.SET_NULL, null=True, blank=True,
    )
    created_at = models.DateTimeField(_("問い合わせ日時"), default=timezone.now)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("問い合わせ")
        verbose_name_plural = _("問い合わせ")

    def __str__(self):
        return self.subject
