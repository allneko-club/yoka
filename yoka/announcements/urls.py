from django.urls import path

from . import views

app_name = "announcements"
urlpatterns = [
    path("", views.AnnouncementListView.as_view(), name="announcement_list"),
    path("<int:pk>/", views.AnnouncementDetailView.as_view(), name="announcement_detail"),
]