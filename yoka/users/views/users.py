import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from yoka.forum.models import Reply
from yoka.users.forms import AccountUpdateForm, EmailUpdateForm, UserCreationForm

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(CreateView):
    """アカウント登録"""
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")
    extra_context = {"title": gettext_lazy("登録フォーム")}

    def form_valid(self, form):
        messages.info(self.request, _("アカウントを作成しました。"))
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UserDetailView(ListView):
    """ユーザープロフィール"""
    model = Reply
    page_size = 50
    context_object_name = "replies"
    template_name = "users/user_detail.html"

    def get_queryset(self):
        return Reply.objects.select_related("thread").visible().filter(user__id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.kwargs["pk"], is_active=True)
        context["title"] = _("%sのプロフィール") % user.username
        context["user"] = user
        return context


@method_decorator(login_required, name="dispatch")
class MyPageView(TemplateView):
    """マイページ"""
    template_name = "users/mypage.html"
    extra_context = {"title": gettext_lazy("マイページ")}


@method_decorator(login_required, name="dispatch")
class AccountUpdateView(UpdateView):
    """アカウント変更"""
    model = User
    form_class = AccountUpdateForm
    success_url = reverse_lazy("users:mypage")
    extra_context = {"title": gettext_lazy("アカウント編集")}

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.info(self.request, _("プロフィールを更新しました。"))
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class AccountDeleteView(DeleteView):
    """アカウント削除"""
    model = User
    template_name = "users/delete_confirm.html"
    success_url = reverse_lazy("users:account_delete_complete")
    extra_context = {"title": gettext_lazy("退会")}

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        logout(self.request)
        success_url = self.get_success_url()
        self.object.deactivate()
        return HttpResponseRedirect(success_url)


@method_decorator(login_required, name="dispatch")
class EmailUpdateView(UpdateView):
    """メールアドレス変更"""
    model = User
    form_class = EmailUpdateForm
    template_name = "users/email_form.html"
    success_url = reverse_lazy("users:mypage")
    extra_context = {"title": gettext_lazy("メールアドレス変更フォーム")}

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.info(self.request, _("メールアドレスを変更しました。"))
        return super().form_valid(form)
