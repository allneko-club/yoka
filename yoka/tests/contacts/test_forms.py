from django.test import TestCase

from yoka.contacts.models import ContactStatus
from yoka.tests.factories import ContactStatusFactory


class TestContactForm(TestCase):
    """ContactFormクラスのテスト"""

    def test_ordering(self):
        """並び順のテスト"""
        self.status2 = ContactStatusFactory(rank=2)
        self.status3 = ContactStatusFactory(rank=3)
        self.status1 = ContactStatusFactory(rank=1)
        statuses = ContactStatus.objects.all()
        self.assertEqual(statuses[0].rank, 1)
        self.assertEqual(statuses[1].rank, 2)
        self.assertEqual(statuses[2].rank, 3)
