from urllib.parse import parse_qs, urlencode, urlparse

from django import template

register = template.Library()


@register.filter
def index(list_, i):
    """
    https://stackoverflow.com/questions/4651172/reference-list-item-by-index-within-django-template
    リストのインデックスアクセスができる。
    {{ my_list|index:x }}
    """
    return list_[i]


@register.filter
def dict_value(dict_, key):
    """
    dictのvalueにアクセスができる。
    {{ my_list|value:x }}
    """
    return dict_[key]


@register.filter
def selected_text(choices, selected_value):
    """
    selectフォームで選択した文字列を取得する
    例) {{ form.field_name.field.choices|selected_text:form.field_name.data }}
    :param choices: ModelChoiceIterator
    :param selected_value: str
    :return:
    """
    for value, text in choices:
        if str(value) == selected_value:
            return text
    return ""


@register.inclusion_tag('components/pagination.html', takes_context=True)
def get_pagination(context, first_last_amount=2, before_after_amount=4):
    page_obj = context['page_obj']
    paginator = context['paginator']
    page_numbers = []

    # Pages before current page
    if page_obj.number > first_last_amount + before_after_amount:
        for i in range(1, first_last_amount + 1):
            page_numbers.append(i)

        if first_last_amount + before_after_amount + 1 != paginator.num_pages:
            page_numbers.append(None)

        for i in range(page_obj.number - before_after_amount, page_obj.number):
            page_numbers.append(i)

    else:
        for i in range(1, page_obj.number):
            page_numbers.append(i)

    # Current page and pages after current page
    if page_obj.number + first_last_amount + before_after_amount < paginator.num_pages:
        for i in range(page_obj.number, page_obj.number + before_after_amount + 1):
            page_numbers.append(i)

        page_numbers.append(None)

        for i in range(paginator.num_pages - first_last_amount + 1, paginator.num_pages + 1):
            page_numbers.append(i)

    else:
        for i in range(page_obj.number, paginator.num_pages + 1):
            page_numbers.append(i)

    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj'],
        'page_numbers': page_numbers,
        'is_paginated': context['is_paginated'],
        'request': context['request'],
    }


@register.simple_tag
def get_page_url(request, page=None, ordering=None):
    qs = parse_qs(urlparse(request.get_full_path()).query)
    if page:
        qs["page"] = [page]
    if ordering:
        qs["ordering"] = [ordering]
    return f"{request.path}?{urlencode(qs, True)}" if qs else request.path
