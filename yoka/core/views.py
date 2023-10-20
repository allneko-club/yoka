from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HowToUseView(TemplateView):
    """使い方ページ"""
    template_name = "core/how-to-use.html"
    extra_context = {"title": _("使い方")}


class RuleView(TemplateView):
    """利用規約ページ"""
    template_name = "core/rule.html"
    extra_context = {"title": _("利用規約")}
