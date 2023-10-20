from datetime import UTC, datetime

from django.test import TestCase

from yoka.announcements.models import Announcement
from yoka.tests.factories import AnnouncementFactory


class TestAnnouncementQueryset(TestCase):
    """AnnouncementQuerysetクラスのテスト"""

    def test_visible(self):
        not_visible = AnnouncementFactory(release_date=datetime(9999, 12, 31, tzinfo=UTC))
        visible = AnnouncementFactory(release_date=datetime(2000, 1, 3, tzinfo=UTC))
        objs = list(Announcement.objects.visible())
        self.assertEqual(objs, [visible])


class TestAnnouncement(TestCase):
    """Announcementクラスのテスト"""

    def test_ordering(self):
        obj1 = AnnouncementFactory(release_date=datetime(2000, 1, 1, tzinfo=UTC))
        obj2 = AnnouncementFactory(release_date=datetime(2000, 1, 3, tzinfo=UTC))
        obj3 = AnnouncementFactory(release_date=datetime(2000, 1, 2, tzinfo=UTC))
        objs = list(Announcement.objects.all())

        self.assertEqual(objs, [obj2, obj3, obj1])
