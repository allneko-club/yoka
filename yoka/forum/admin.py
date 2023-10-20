from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Reply, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "title", "user", "view_count", "reply_count", "is_hidden", "closed",
    )
    fields = ("title", "user", "content", "is_hidden", "closed")
    search_fields = ("title", "user__username", "user__email")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "is_hidden")
    fields = ("user", "content", "is_hidden")
    search_fields = ("user__username", "user__email")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    def number_of_threads(self, obj):
        threads = Thread.objects.filter(category=obj)
        return f"{threads.count()}({threads.visible().count()})"

    number_of_threads.short_description = _("スレッド数 [合計(公開中)]")

    list_display = ("title", "number_of_threads")
    search_fields = ("title",)
