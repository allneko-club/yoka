"""
"""
from datetime import UTC, datetime

from django.test import TestCase
from django.urls import reverse

from yoka.tests.factories import AnnouncementFactory


class TestAnnouncementListView(TestCase):

    def setUp(self):
        self.viewname = "announcements:announcement_list"

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["paginator"].count, 0)
        self.assertTemplateUsed(res, "announcements/announcement_list.html")

    def test_ordering(self):
        obj1 = AnnouncementFactory(release_date=datetime(2000, 1, 1, tzinfo=UTC))
        obj2 = AnnouncementFactory(release_date=datetime(2000, 1, 3, tzinfo=UTC))
        obj3 = AnnouncementFactory(release_date=datetime(2000, 1, 2, tzinfo=UTC))

        res = self.client.get(reverse(self.viewname))
        self.assertEqual(list(res.context["object_list"]), [obj2, obj3, obj1])

    def test_get_queryset(self):
        not_visible = AnnouncementFactory(release_date=datetime(9999, 12, 31, tzinfo=UTC))
        visible = AnnouncementFactory(release_date=datetime(2000, 1, 3, tzinfo=UTC))

        res = self.client.get(reverse(self.viewname))
        self.assertEqual(list(res.context["object_list"]), [visible])
