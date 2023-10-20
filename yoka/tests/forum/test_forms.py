from django.test import TestCase

from yoka.forum.forms import CreateThreadForm, ReplyForm, UpdateThreadForm
from yoka.tests.factories import CategoryFactory, ThreadFactory, UserFactory


class TestCreateThreadForm(TestCase):
    """CreateThreadFormクラスのテスト"""

    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()

    def test_save(self):
        """save()のテスト"""
        data = {
            "title": "thread title",
            "category": self.category.id,
            "handle_name": "Rin",
            "content": "thread title",
        }
        form = CreateThreadForm(data, user=self.user)
        obj = form.save()
        self.assertEqual(obj.title, data["title"])
        self.assertEqual(obj.category, self.category)
        self.assertEqual(obj.handle_name, data["handle_name"])
        self.assertEqual(obj.content, data["content"])


class TestUpdateThreadForm(TestCase):
    """UpdateThreadFormクラスのテスト"""

    def setUp(self):
        self.category = CategoryFactory()
        self.thread = ThreadFactory()

    def test_save(self):
        """save()のテスト"""
        data = {
            "title": "thread title",
            "category": self.category.id,
            "handle_name": "Rin",
            "content": "thread title",
        }
        form = UpdateThreadForm(data, instance=self.thread)
        obj = form.save()
        self.assertEqual(obj.title, data["title"])
        self.assertEqual(obj.category, self.category)
        self.assertEqual(obj.handle_name, data["handle_name"])
        self.assertEqual(obj.content, data["content"])


class TestReplyForm(TestCase):
    """ReplyFormクラスのテスト"""

    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.thread = ThreadFactory()

    def test_save(self):
        """save()のテスト"""
        data = {
            "handle_name": "Rin",
            "content": "this is reply.",
        }
        form = ReplyForm(data, user=self.user, thread_id=self.thread.id)
        obj = form.save()
        self.assertEqual(obj.user, self.user)
        self.assertEqual(obj.thread, self.thread)
        self.assertEqual(obj.handle_name, data["handle_name"])
        self.assertEqual(obj.content, data["content"])
