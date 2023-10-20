from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("how-to-use/", views.HowToUseView.as_view(), name="how_to_use"),
    path("rule/", views.RuleView.as_view(), name="rule"),
]
