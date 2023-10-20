from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from yoka.announcements.models import Announcement


class AnnouncementListView(ListView):
    """
    お知らせ一覧ページ
    """
    model = Announcement
    ordering = "-release_date"
    paginate_by = 30
    extra_context = {"title": _("お知らせ一覧")}

    def get_queryset(self):
        queryset = Announcement.objects.visible()
        return queryset


class AnnouncementDetailView(DetailView):
    """
    お知らせ詳細ページ
    """
    model = Announcement
    extra_context = {"title": _("お知らせ詳細")}
