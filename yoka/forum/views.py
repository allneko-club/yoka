from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, gettext_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import CreateThreadForm, ReplyForm, UpdateThreadForm
from .models import Category, Reply, Thread

User = get_user_model()


class IndexView(ListView):
    """ホームページ"""
    model = Thread
    paginate_by = 50
    template_name = "forum/index.html"
    extra_context = {"title": gettext_lazy("ホーム")}
    context_object_name = "threads"

    def get_queryset(self):
        return Thread.objects.visible().select_related("user", "category")


class ThreadListView(ListView):
    model = Thread
    paginate_by = 50
    template_name = "forum/thread_list.html"
    extra_context = {"title": gettext_lazy("スレッド一覧")}

    def get_queryset(self):
        return Thread.objects.visible().select_related("user", "category")


class CategoryThreadListView(ThreadListView):

    def get_queryset(self):
        return (
            Thread.objects.visible()
            .filter(category__slug=self.kwargs.get("slug"))
            .select_related("user", "category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs.get("slug"))
        context["category"] = category
        context["title"] = category.title
        return context


@method_decorator(login_required, name="post")
class ReplyListInThreadView(FormMixin, ListView):
    """スレッドの詳細、返信一覧、返信フォームがあるページ"""
    model = Reply
    paginate_by = 50
    template_name = "forum/thread_detail.html"
    context_object_name = "replies"
    form_class = ReplyForm

    @property
    def thread_id(self):
        return self.kwargs.get("pk")

    def get_queryset(self):
        return (
            Reply.objects.visible()
            .filter(thread_id=self.thread_id)
            .select_related("user")
            .order_by("-create_date")
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["thread_id"] = self.kwargs.get("pk")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "thread" in kwargs:
            # post()の時に実行される
            context["thread"] = kwargs["thread"]
        else:
            # get()の時に実行される
            thread = Thread.objects.visible().get(pk=self.thread_id)
            thread.increase_view_count()
            context["thread"] = thread

        context["title"] = context["thread"].title
        return context

    def get_success_url(self):
        return reverse("forum:thread_detail", kwargs={"pk": self.thread_id})

    def post(self, request, *args, **kwargs):
        thread = Thread.objects.visible().get(pk=self.thread_id)

        if thread.closed:
            messages.warning(self.request, _("このスレッドは閉鎖されました。"))
            return HttpResponseRedirect(self.get_success_url())

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, thread)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, thread):
        self.object_list = self.get_queryset()
        ctx = self.get_context_data(form=form, thread=thread)
        if self.request.POST.get("next") == "confirm":
            return render(self.request, "forum/reply_confirm.html", ctx)
        if self.request.POST.get("next") == "submit":
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(self.request, "forum/thread_detail.html", ctx)


@method_decorator(login_required, name="dispatch")
class CreateThreadView(CreateView):
    model = Thread
    form_class = CreateThreadForm
    template_name = "forum/thread_form.html"
    extra_context = {"title": gettext_lazy("スレッド作成")}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        ctx = self.get_context_data(form=form)

        if self.request.POST.get("next") == "confirm":
            return render(self.request, "forum/thread_confirm.html", ctx)
        if self.request.POST.get("next") == "submit":
            return super().form_valid(form)
        else:
            return render(self.request, "forum/thread_form.html", ctx)

    def get_success_url(self):
        return reverse("forum:thread_detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required, name="dispatch")
class UpdateThreadView(UpdateView):
    model = Thread
    template_name = "forum/thread_form.html"
    extra_context = {"title": gettext_lazy("スレッド編集")}
    form_class = UpdateThreadForm

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.reply_count > 0:
            messages.warning(self.request, _("リプライ済みのスレッドは編集できません。"))
            return HttpResponseRedirect(self.get_success_url())

        if self.object.user.id != request.user.id:
            # url直打ち以外は実行されない処理のため403を返す
            return HttpResponseForbidden(_("自分で作成していないスレッドは編集できません。"))

        return response

    def form_valid(self, form):
        ctx = self.get_context_data(form=form)
        if self.request.POST.get("next") == "confirm":
            return render(self.request, "forum/thread_confirm.html", ctx)
        if self.request.POST.get("next") == "submit":
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("forum:thread_detail", kwargs={"pk": self.object.pk})


class SearchThreadView(ListView):
    model = Thread
    paginate_by = 50
    template_name = "forum/thread_search_list.html"
    context_object_name = "threads"
    extra_context = {"title": gettext_lazy("スレッド検索")}
    search_url_kwarg = "keywords"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.search_url_kwarg] = self.request.GET.get(self.search_url_kwarg, "")
        return context

    def get_ordering(self):
        query_order = self.request.GET.get("order", "")
        if query_order in ["-create_date", "create_date"]:
            return query_order
        return "-create_date"

    def get_queryset(self):
        keywords = self.request.GET.get(self.search_url_kwarg, "")
        return (
            Thread.objects.visible().filter(title__icontains=keywords)
            .select_related("user", "category")
            .order_by(self.get_ordering())
        )
