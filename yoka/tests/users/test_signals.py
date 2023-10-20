from django.contrib.auth.signals import user_logged_in
from django.test import RequestFactory, TestCase
from django.urls import reverse

from yoka.tests.factories import UserFactory
from yoka.users.models import LoginHistory


class TestSignals(TestCase):

    def test_create_login_history(self):
        user = UserFactory()
        factory = RequestFactory()
        user_agent = "Mozilla/5.0"
        data = {
            "username": user.username,
            "password": "a9XT7Kqb",
        }
        request = factory.post(reverse("users:login"), data, HTTP_USER_AGENT=user_agent)
        user_logged_in.send(
            sender=user.__class__,
            request=request,
            user=user,
        )
        histories = LoginHistory.objects.all()
        self.assertEqual(len(histories), 1)
        self.assertEqual(histories[0].user, user)
        self.assertEqual(histories[0].user_agent, user_agent)
