from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from . import views

app_name = "contacts"
urlpatterns = [
    path("", views.ContactCreateView.as_view(), name="contact_form"),
    path("done/", views.ContactDoneView.as_view(), name="contact_done"),
]
