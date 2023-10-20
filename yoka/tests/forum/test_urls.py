from django.test import TestCase
from django.urls import reverse


class TestForumURLs(TestCase):
    """urls.pyのテスト"""

    def test_home_url(self):
        self.assertURLEqual(reverse("home"), "/")

    def test_thread_list_url(self):
        self.assertURLEqual(reverse("forum:thread_list"), "/forum/thread/")

    def test_category_threads_url(self):
        self.assertURLEqual(reverse("forum:category_threads", kwargs={"slug": "life"}), "/forum/thread/category/life/")

    def test_thread_detail_url(self):
        uuid = "c9403065-10d8-4e3b-bb7c-b2f7b235a8a3"
        self.assertURLEqual(reverse("forum:thread_detail", kwargs={"pk": uuid}), f"/forum/thread/{uuid}/")

    def test_create_thread_url(self):
        self.assertURLEqual(reverse("forum:create_thread"), "/forum/thread/create/")

    def test_update_thread_url(self):
        uuid = "c9403065-10d8-4e3b-bb7c-b2f7b235a8a3"
        self.assertURLEqual(reverse("forum:update_thread", kwargs={"pk": uuid}), f"/forum/thread/{uuid}/update/")

    def test_search_thread_url(self):
        self.assertURLEqual(reverse("forum:search_thread"), "/forum/search/thread/")
