from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from yoka.tests.factories import UserFactory
from yoka.users.forms import AccountUpdateForm, EmailUpdateForm
from yoka.users.models import Address

User = get_user_model()


class TestAccountUpdateForm(TestCase):
    fixtures = ["address"]

    def setUp(self):
        address = Address.objects.get(id=1)
        self.user = UserFactory()

    def test_invalid_choice(self):
        data = {
            "address": -1,
            "sex": "invalid",
        }
        expected = [_("選択肢の中から選んでください")]
        form = AccountUpdateForm(data, instance=self.user)
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors["address"], expected)
        self.assertEqual(form.errors["sex"], expected)

    def test_save(self):
        data = {
            "address": 2,
            "sex": "女性",
        }
        form = AccountUpdateForm(data, instance=self.user)
        obj = form.save()
        self.assertEqual(obj.address_id, data["address"])
        self.assertEqual(obj.sex, data["sex"])


class TestEmailUpdateForm(TestCase):
    fixtures = ["address"]

    def setUp(self):
        self.user = UserFactory()

    def test_save(self):
        data = {"email": "update@example.com"}
        form = EmailUpdateForm(data, instance=self.user)
        obj = form.save()
        self.assertEqual(obj.email, data["email"])
