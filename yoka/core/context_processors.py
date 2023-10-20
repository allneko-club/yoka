from django.conf import settings


def yoka_processor(request):
    """テンプレートで使うためのsettings"""
    return {
        'DEBUG': settings.DEBUG,
        "COMPANY_NAME": settings.COMPANY_NAME,
        "DEFAULT_HANDLE_NAME": settings.DEFAULT_HANDLE_NAME,
        "SITE_NAME": settings.SITE_NAME,
    }
