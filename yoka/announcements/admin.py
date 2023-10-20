from django.contrib import admin

from yoka.announcements.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "release_date"]
    readonly_fields = ["update_date", "update_user", "create_date", "create_user"]

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user
        if not change:
            obj.create_user = request.user
        super().save_model(request, obj, form, change)
