from django.test import TestCase
from django.urls import reverse


class TestAnnouncementsURLs(TestCase):
    """urls.pyのテスト"""

    def test_announcement_list_url(self):
        self.assertURLEqual(reverse("announcements:announcement_list"), "/announcement/")

    def test_announcement_detail_url(self):
        self.assertURLEqual(reverse("announcements:announcement_detail", kwargs={"pk": 1}), "/announcement/1/")
