import logging

from django.core.mail import send_mail
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


def send_sign_up_done_mail(email, **kwargs):
    """アカウント登録完了時に送るメール"""
    send_mail(
        _('アカウント登録完了'),
        _('アカウント登録が完了しました'),
        None,
        [email],
        fail_silently=False,
    )


def send_email_changed_mail(email, **kwargs):
    """メールアドレス変更時に送るメール"""
    send_mail(
        _('メールアドレス変更受付'),
        _('メールアドレスの変更を受付ました'),
        None,
        [email],
        fail_silently=False,
    )
