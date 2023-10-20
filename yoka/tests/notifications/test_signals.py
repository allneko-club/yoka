from django.conf import settings
from django.core import mail
from django.test import TestCase

from yoka.contacts.models import Contact
from yoka.contacts.signals import contact_done
from yoka.tests.factories import UserFactory
from yoka.users.signals import deactivate_user


class TestSignals(TestCase):

    def setUp(self):
        pass

    def test_send_deactivated_mail(self):
        user = UserFactory()
        deactivate_user.send(
            sender=user.__class__,
            email=user.email,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'アカウント削除処理完了')
        self.assertEqual(mail.outbox[0].body, 'アカウント削除処理が完了しました')
        self.assertEqual(mail.outbox[0].to, [user.email])

    def test_send_contact_done_mail(self):
        contact_done.send(
            sender=Contact,
            email="test@example.com",
            subject="テストタイトル",
            message="テスト本文",
        )

        self.assertEqual(len(mail.outbox), 2)

        # 管理者宛メール
        to_admin = mail.outbox[0]
        self.assertEqual(to_admin.subject, f"{settings.EMAIL_SUBJECT_PREFIX}テストタイトル")
        self.assertEqual(to_admin.body, "テスト本文")
        expected = [admin[1] for admin in settings.ADMINS]
        self.assertEqual(to_admin.to, expected)

        # 問い合わせ宛向けメール
        to_user = mail.outbox[1]
        self.assertEqual(to_user.subject, "お問い合わせありがとうございます。")
        self.assertEqual(to_user.body, "お問い合わせを受け付けました。返信まで2〜３営業日かかります。")
        self.assertEqual(to_user.to, ["test@example.com"])
