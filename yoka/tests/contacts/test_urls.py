from django.test import TestCase
from django.urls import reverse


class TestContactURLs(TestCase):
    """urls.pyのテスト"""

    def test_contact_form_url(self):
        self.assertURLEqual(reverse("contacts:contact_form"), "/contact/")

    def test_contact_done_url(self):
        self.assertURLEqual(reverse("contacts:contact_done"), "/contact/done/")
