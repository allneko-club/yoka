from django import template

from yoka.forum.models import Category

register = template.Library()


@register.inclusion_tag('components/categories.html')
def get_categories():
    return {"categories": Category.objects.all()}
