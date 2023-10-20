import uuid

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    """
    居住地のモデル
    """
    name = models.CharField(_("名前"), max_length=16, unique=True)
    rank = models.PositiveIntegerField(_("表示順"), unique=True)

    class Meta:
        ordering = ["rank"]
        verbose_name = _("居住地")
        verbose_name_plural = _("居住地")

    def __str__(self):
        return self.name


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class UserManager(DjangoUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()


class User(AbstractUser):
    """ユーザーモデル"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    SEX_CHOICES = [
        ("男性", "男性"),
        ("女性", "女性"),
    ]
    REQUIRED_FIELDS = ["email"]

    first_name = None
    last_name = None
    email = models.EmailField(_("メールアドレス"), unique=True)
    sex = models.CharField(_("性別"), choices=SEX_CHOICES, max_length=10, null=True, blank=True)
    address = models.ForeignKey(Address, verbose_name=_("居住地"), on_delete=models.SET_NULL, null=True, blank=True)
    birthday = models.DateField(_("生年月日"), null=True, blank=True)
    accept_rule = models.BooleanField(_("利用規約同意フラグ"), default=False)

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"pk": self.id})

    def deactivate(self):
        """論理削除"""
        self.is_active = False
        self.save()


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_agent = models.TextField()
    login_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}_{self.login_date}"

    class Meta:
        ordering = ["-login_date"]
        verbose_name = _("ログイン履歴")
        verbose_name_plural = _("ログイン履歴")
