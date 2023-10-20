from yoka.forum.models import Reply, Thread
from yoka.tests.factories import ReplyFactory, ThreadFactory
from yoka.tests.utils.views import ModelsTestCase


class TestThreadQuerySet(ModelsTestCase):
    """ThreadQuerySetクラスのテスト"""

    def test_visible(self):
        """visible()のテスト"""
        ThreadFactory(is_hidden=False)
        ThreadFactory(is_hidden=True)
        threads = Thread.objects.visible()

        self.assertEqual(len(threads), 1)
        self.assertFalse(threads[0].is_hidden)


class TestThread(ModelsTestCase):
    """Threadクラスのテスト"""

    def test_get_reply_count(self):
        """get_reply_count()のテスト"""
        thread = ThreadFactory()
        ReplyFactory(thread=thread)
        thread.refresh_from_db()
        self.assertEqual(thread.get_reply_count(), 1)

    def test_increase_view_count(self):
        """increase_view_count()のテスト"""
        thread = ThreadFactory()
        thread.increase_view_count()
        thread.refresh_from_db()
        self.assertEqual(thread.view_count, 1)


class TestReplyQuerySet(ModelsTestCase):
    """ReplyQuerySetクラスのテスト"""

    def test_visible(self):
        """visible()のテスト"""
        ReplyFactory(is_hidden=False)
        ReplyFactory(is_hidden=True)
        replies = Reply.objects.visible()

        self.assertEqual(len(replies), 1)
        self.assertFalse(replies[0].is_hidden)
