from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext as _

from yoka.forum.models import Reply, Thread
from yoka.tests.factories import CategoryFactory, ReplyFactory, ThreadFactory
from yoka.tests.utils.views import AuthViewsTestCase


class TestHomeView(AuthViewsTestCase):

    def setUp(self):
        self.viewname = "home"

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/index.html")

    def test_get_queryset(self):
        not_hidden_thread = ThreadFactory(is_hidden=False)
        ThreadFactory(is_hidden=True)
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(len(res.context["threads"]), 1)
        self.assertEqual(res.context["threads"][0], not_hidden_thread)


class TestThreadListView(AuthViewsTestCase):

    def setUp(self):
        self.viewname = "forum:thread_list"
        self.not_hidden_thread = ThreadFactory(is_hidden=False)
        self.hidden_thread = ThreadFactory(is_hidden=True)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_list.html")

    def test_get_queryset(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(len(res.context["page_obj"]), 1)
        self.assertEqual(res.context["page_obj"][0], self.not_hidden_thread)


class TestCategoryThreadListView(AuthViewsTestCase):

    def setUp(self):
        self.viewname = "forum:category_threads"
        self.category = CategoryFactory()
        self.not_hidden_thread = ThreadFactory(category=self.category, is_hidden=False)
        self.hidden_thread = ThreadFactory(category=self.category, is_hidden=True)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname, kwargs={"slug": self.category.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_list.html")

    def test_get_queryset(self):
        res = self.client.get(reverse(self.viewname, kwargs={"slug": self.category.slug}))
        self.assertEqual(len(res.context["page_obj"]), 1)
        self.assertEqual(res.context["page_obj"][0], self.not_hidden_thread)

    def test_get_context_data(self):
        res = self.client.get(reverse(self.viewname, kwargs={"slug": self.category.slug}))
        self.assertEqual(res.context["category"], self.category)
        self.assertEqual(res.context["title"], self.category.title)


class TestReplyListInThreadView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "forum:thread_detail"
        self.category = CategoryFactory()
        self.thread = ThreadFactory(category=self.category)
        self.reply1 = ReplyFactory(thread=self.thread, is_hidden=False)
        self.reply2 = ReplyFactory(thread=self.thread, is_hidden=False)
        self.reply3 = ReplyFactory(thread=self.thread, is_hidden=True)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_detail.html")

    def test_get_queryset(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertEqual(len(res.context["replies"]), 2)
        self.assertEqual(res.context["replies"][0], self.reply2)
        self.assertEqual(res.context["replies"][1], self.reply1)

    def test_get_context_data(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.thread.refresh_from_db()
        self.assertEqual(res.context["thread"], self.thread)
        self.assertEqual(res.context["title"], self.thread.title)
        self.assertEqual(self.thread.view_count, 1)

    def test_login_required(self):
        self.logout()
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertEqual(res.status_code, 302)

    def test_post_confirm(self):
        """
        入力確認postのチェック
        """
        data = {
            "handle_name": "Rei",
            "content": "テスト 本文",
            "next": "confirm",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/reply_confirm.html")

    def test_post_back(self):
        """
        入力確認画面から戻るボタンをクリックした時のテスト
        """
        data = {
            "handle_name": "Rei",
            "content": "テスト 本文",
            "next":  "back",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_detail.html")

    def test_post_submit(self):
        """
        入力確認画面から送信ボタンをクリックした時のテスト
        """
        data = {
            "handle_name": "Rei",
            "content": "テスト 本文",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        self.assertRedirects(res, reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertTrue(
            Reply.objects.filter(handle_name=data["handle_name"], content=data["content"]).exists()
        )

    def test_post_thread_closed(self):
        """
        閉鎖されているスレッドに返信する場合のテスト
        """
        data = {
            "handle_name": "Rei",
            "content": "テスト 本文",
            "next": "confirm",
        }
        hidden_thread = ThreadFactory(closed=True, category=self.category)
        res = self.client.post(reverse(self.viewname, kwargs={"pk": hidden_thread.id}), data)
        self.assertRedirects(res, reverse(self.viewname, kwargs={"pk": hidden_thread.id}))

        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("このスレッドは閉鎖されました。"))


class TestCreateThreadView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "forum:create_thread"
        self.category = CategoryFactory()

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_form.html")

    def test_post_confirm(self):
        """
        入力確認postのチェック
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next": "confirm",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_confirm.html")

    def test_post_back(self):
        """
        入力確認画面から戻るボタンをクリックした時のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "back",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_form.html")

    def test_post_submit(self):
        """
        入力確認画面から送信ボタンをクリックした時のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname), data)
        threads = Thread.objects.filter(title=data["title"])
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(threads), 1)

    def test_get_success_url(self):
        """
        get_success_url()のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname), data)
        threads = Thread.objects.filter(title=data["title"])
        self.assertRedirects(res, reverse("forum:thread_detail", kwargs={"pk": threads[0].id}))


class TestUpdateThreadView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "forum:update_thread"
        self.thread = ThreadFactory(user=self.user)
        self.category = self.thread.category

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_form.html")

    def test_get_replied_thread(self):
        """リプライ済みスレッドを編集しようとする場合のテスト"""
        self.thread.reply_count = 1
        self.thread.save()
        self.thread.refresh_from_db()
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.thread.id}))
        self.assertRedirects(res, reverse("forum:thread_detail", kwargs={"pk": self.thread.id}))

        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("リプライ済みのスレッドは編集できません。"))

    def test_other_user_get(self):
        """スレッドの作成者以外がページにアクセスした場合のテスト"""
        thread = ThreadFactory()
        res = self.client.get(reverse(self.viewname, kwargs={"pk": thread.id}))
        self.assertEqual(res.status_code, 403)

    def test_post_confirm(self):
        """
        入力確認postのチェック
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next": "confirm",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_confirm.html")

    def test_post_back(self):
        """
        入力確認画面から戻るボタンをクリックした時のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "back",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_form.html")

    def test_post_submit(self):
        """
        入力確認画面から送信ボタンをクリックした時のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        threads = Thread.objects.filter(title=data["title"])
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(threads), 1)

    def test_get_success_url(self):
        """
        get_success_url()のテスト
        """
        data = {
            "title": "title sample",
            "category": self.category.id,
            "handle_name": "Rei",
            "content": "content sample",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname, kwargs={"pk": self.thread.id}), data)
        threads = Thread.objects.filter(title=data["title"])
        self.assertRedirects(res, reverse("forum:thread_detail", kwargs={"pk": threads[0].id}))


class TestSearchThreadView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "forum:search_thread"
        self.thread1 = ThreadFactory(title="life_food_travel")
        self.thread2 = ThreadFactory(title="job hobby")
        self.thread3 = ThreadFactory(title="friend travel")
        self.hidden_thread = ThreadFactory(is_hidden=True, title="travel hobby")

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "forum/thread_search_list.html")

    def test_get_context_data(self):
        res = self.client.get(reverse(self.viewname) + "?keywords=life")
        self.assertEqual(res.context["keywords"], "life")

    def test_get_ordering_default(self):
        res = self.client.get(reverse(self.viewname))
        threads = res.context["threads"]
        self.assertEqual(len(threads), 3)
        self.assertTrue(threads[1].create_date < threads[0].create_date)

    def test_get_ordering_create_date_des(self):
        res = self.client.get(reverse(self.viewname) + "?order=create_date")
        threads = res.context["threads"]
        self.assertEqual(len(threads), 3)
        self.assertTrue(threads[0].create_date < threads[1].create_date)

    def test_get_ordering_create_date_asc(self):
        res = self.client.get(reverse(self.viewname) + "?order=create_date")
        threads = res.context["threads"]
        self.assertEqual(len(threads), 3)
        self.assertTrue(threads[0].create_date < threads[1].create_date)

    def test_get_queryset(self):
        """検索ワードがある時のデータ取得テスト"""
        res = self.client.get(reverse(self.viewname) + "?keywords=travel")
        threads = res.context["threads"]
        self.assertEqual(len(threads), 2)
        self.assertEqual(threads[0], self.thread3)
        self.assertEqual(threads[1], self.thread1)
