from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.translation import gettext as _

from yoka.tests.factories import UserFactory
from yoka.tests.utils.views import AuthViewsTestCase

User = get_user_model()


class TestLogoutView(AuthViewsTestCase):

    def setUp(self):
        self.viewname = "users:logout"

    def test_login_required(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)


class TestPasswordChangeView(AuthViewsTestCase):

    def setUp(self):
        self.credentials = {"username": "test_user", "password": "a9XT7Kqb"}
        self.user = UserFactory(**self.credentials)
        self.client.login(**self.credentials)
        self.viewname = "users:password_change"

    def test_login_required(self):
        self.logout()
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_form.html")

    def test_simple_post(self):
        res = self.client.post(
            reverse(self.viewname),
            {
                'old_password': self.credentials["password"],
                'new_password1': 'Tc7FNt5W',
                'new_password2': 'Tc7FNt5W',
            },
        )
        self.assertRedirects(res, reverse('users:mypage'))
        messages = list(get_messages(res.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _("パスワードを変更しました。"))


class TestPasswordChangeDoneView(AuthViewsTestCase):

    def setUp(self):
        self.viewname = "users:password_change_done"

    def test_login_required(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 302)
