import uuid

from django.conf import settings
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

USER_MODEL = settings.AUTH_USER_MODEL


class ThreadQuerySet(models.QuerySet):

    def visible(self):
        return self.filter(is_hidden=False)


class Thread(models.Model):
    """スレッド"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("タイトル"), max_length=120)
    content = models.TextField(_("本文"))
    user = models.ForeignKey(USER_MODEL, related_name="threads", verbose_name=_("ユーザー"), on_delete=models.CASCADE)
    handle_name = models.CharField(_("ハンドルネーム"), max_length=10, null=True, blank=True)
    view_count = models.IntegerField(_("閲覧数"), default=0)
    reply_count = models.IntegerField(_("返信数"), default=0)
    category = models.ForeignKey(
        "Category", related_name="threads", verbose_name=_("カテゴリー"), on_delete=models.CASCADE
    )
    is_hidden = models.BooleanField(_("非表示フラグ"), default=False)
    closed = models.BooleanField(_("閉鎖"), default=False)
    update_date = models.DateTimeField(_("更新日時"), auto_now=True)
    create_date = models.DateTimeField(_("投稿日時"), default=timezone.now)

    objects = ThreadQuerySet.as_manager()

    class Meta:
        verbose_name = _("スレッド")
        verbose_name_plural = _("スレッド")
        ordering = ["-create_date"]

    def __str__(self):
        return self.title

    def get_reply_count(self):
        return self.replies.visible().count()

    def increase_view_count(self):
        Thread.objects.filter(pk=self.id).update(view_count=F("view_count") + 1)


class ReplyQuerySet(models.QuerySet):

    def visible(self):
        return self.filter(is_hidden=False)


class Reply(models.Model):
    """返信（リプライ）"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        "forum.Thread", related_name="replies", verbose_name=_("スレッド"), on_delete=models.CASCADE,
    )
    user = models.ForeignKey(USER_MODEL, related_name="posts", verbose_name=_("ユーザー"), on_delete=models.CASCADE)
    handle_name = models.CharField(_("ハンドルネーム"), max_length=10, default="", blank=True)
    content = models.TextField(_("本文"))
    is_hidden = models.BooleanField(_("非表示フラグ"), default=False)
    update_date = models.DateTimeField(_("更新日時"), auto_now=True)
    create_date = models.DateTimeField(_("投稿日時"), default=timezone.now)

    objects = ReplyQuerySet.as_manager()

    class Meta:
        ordering = ["-create_date"]
        verbose_name = _("返信")
        verbose_name_plural = _("返信")

    def __str__(self):
        return f"{self.thread.title}"


class Category(models.Model):
    """カテゴリー"""
    slug = models.SlugField(max_length=20, unique=True)
    title = models.CharField(_("タイトル"), max_length=30, unique=True)
    description = models.TextField(_("説明"), default="", blank=True)
    rank = models.PositiveIntegerField(_("表示順"), unique=True)

    class Meta:
        ordering = ["rank"]
        verbose_name = _("カテゴリー")
        verbose_name_plural = _("カテゴリー")

    def __str__(self):
        return self.title
