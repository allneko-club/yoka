from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from yoka.tests.factories import UserFactory
from yoka.users.forms import UserCreationForm

User = get_user_model()


class TestUserCreationForm(TestCase):
    """
    UserCreationFormのテスト
    """

    fixtures = ["address"]

    def setUp(self):
        self.user = UserFactory()

    def test_username_validation_error_msg(self):
        form = UserCreationForm(
            {
                "username": self.user.username,
                "email": "test@example.com",
                "password1": self.user.password,
                "password2": self.user.password,
                "accept_rule": "on",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors["username"][0], _("このユーザー名は使用できません。"))

    def test_accept_rule_validation_error_msg(self):
        form = UserCreationForm(
            {
                "username": "new_user",
                "email": "test@example.com",
                "password1": "G5hx3bzJ",
                "password2": "G5hx3bzJ",
                "accept_rule": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors["accept_rule"][0], _("利用規約に同意して下さい。"))
