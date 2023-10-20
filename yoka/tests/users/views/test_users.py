from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from yoka.tests.factories import ReplyFactory, UserFactory
from yoka.tests.utils.views import AuthViewsTestCase

User = get_user_model()


class TestRegisterView(TestCase):

    def setUp(self):
        self.viewname = "users:register"

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/register.html")

    def test_simple_post(self):
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "Tc7FNt5W",
            "password2": "Tc7FNt5W",
            "accept_rule": "on",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertRedirects(res, reverse("users:login"))
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("アカウントを作成しました。"))

    def test_register_user(self):
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "password1": "Tc7FNt5W",
            "password2": "Tc7FNt5W",
            "accept_rule": "on",
        }
        self.client.post(reverse(self.viewname), data)
        self.assertTrue(User.objects.filter(username="test_user").exists())


class TestUserDetailView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "users:user_detail"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.user.id}))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.user.id}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/user_detail.html")

    def test_get_not_active_user(self):
        not_active_user = UserFactory(is_active=False)
        res = self.client.get(reverse(self.viewname, kwargs={"pk": not_active_user.id}))
        self.assertEqual(res.status_code, 404)

    def test_get_context_data(self):
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.user.id}))
        self.assertEqual(res.context["user"], self.user)
        self.assertEqual(res.context["title"], f"{self.user.username}のプロフィール")

    def test_get_queryset(self):
        user1 = UserFactory()
        user_reply1 = ReplyFactory(user=self.user)
        user_reply2 = ReplyFactory(thread=user_reply1.thread, user=self.user)
        user1_reply1 = ReplyFactory(thread=user_reply1.thread, user=user1)
        res = self.client.get(reverse(self.viewname, kwargs={"pk": self.user.id}))
        self.assertEqual(len(res.context["replies"]), 2)
        self.assertEqual(list(res.context["replies"]), [user_reply2, user_reply1])


class TestMyPageView(AuthViewsTestCase):

    def setUp(self):
        self.login()
        self.viewname = "users:mypage"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/mypage.html")


class TestAccountUpdateView(AuthViewsTestCase):
    fixtures = ["address"]

    def setUp(self):
        self.login()
        self.viewname = "users:account_update"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/user_form.html")

    def test_simple_post(self):
        data = {
            "address": 1,
            "sex": "女性",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertRedirects(res, reverse("users:mypage"))
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("プロフィールを更新しました。"))

    def test_update_user(self):
        data = {
            "address": 1,
            "sex": "女性",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.address_id, 1)
        self.assertEqual(self.user.sex, "女性")


class TestAccountDeleteView(AuthViewsTestCase):
    def setUp(self):
        self.login()
        self.viewname = "users:account_delete"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/delete_confirm.html")

    def test_simple_post(self):
        res = self.client.post(reverse(self.viewname))
        self.assertRedirects(res, reverse("users:account_delete_complete"))

    def test_delete_user(self):
        res = self.client.post(reverse(self.viewname))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class TestEmailUpdateView(AuthViewsTestCase):
    def setUp(self):
        self.login()
        self.viewname = "users:email_update"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/email_form.html")

    def test_simple_post(self):
        data = {"email": "update@example.com"}
        res = self.client.post(reverse(self.viewname), data)
        self.assertRedirects(res, reverse("users:mypage"))

        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("メールアドレスを変更しました。"))

    def test_update_email(self):
        data = {"email": "update@example.com"}
        res = self.client.post(reverse(self.viewname), data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])
