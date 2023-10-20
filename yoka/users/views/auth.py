"""
djangoの認証ビューを継承してカスタマイズするためのファイル
"""
from django.contrib import messages
from django.contrib.auth import get_user_model, views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, gettext_lazy

from yoka.users.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

User = get_user_model()


class LoginView(views.LoginView):
    form_class = AuthenticationForm
    extra_context = {"title": gettext_lazy("ログイン")}


@method_decorator(login_required, name="dispatch")
class LogoutView(views.LogoutView):
    extra_context = {"title": gettext_lazy("ログアウト")}


class PasswordResetView(views.PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")
    extra_context = {"title": gettext_lazy("パスワードリセット申請フォーム")}


class PasswordResetDoneView(views.PasswordResetDoneView):
    extra_context = {"title": gettext_lazy("パスワードリセット申請完了")}


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
    extra_context = {"title": gettext_lazy("パスワードリセット確認")}


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    extra_context = {"title": gettext_lazy("パスワードリセット完了")}


@method_decorator(login_required, name="dispatch")
class PasswordChangeView(views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:mypage")
    extra_context = {"title": gettext_lazy("パスワード変更フォーム")}

    def form_valid(self, form):
        messages.info(self.request, _("パスワードを変更しました。"))
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class PasswordChangeDoneView(views.PasswordChangeDoneView):
    extra_context = {"title": gettext_lazy("パスワード変更完了")}
