from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.dispatch import receiver

from yoka.contacts.signals import contact_done
from yoka.users.signals import deactivate_user


@receiver(deactivate_user)
def send_deactivated_mail(sender, **kwargs):
    """アカウント削除完了メールを送る"""
    email = kwargs["email"] if "email" in kwargs else None
    if not email:
        return

    send_mail(
        "アカウント削除処理完了",
        "アカウント削除処理が完了しました",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@receiver(contact_done)
def send_contact_done_mail(sender, **kwargs):
    """問い合わせ完了時に管理者と問い合わせ人にメールを送る"""
    email = kwargs["email"]
    subject = kwargs["subject"]
    message = kwargs["message"]

    mail_admins(subject, message)

    send_mail(
        "お問い合わせありがとうございます。",
        "お問い合わせを受け付けました。返信まで2〜３営業日かかります。",
        None,
        [email],
        fail_silently=False,
    )
