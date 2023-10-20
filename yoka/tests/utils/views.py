"""

"""

from django.test import TestCase

from yoka.tests.factories import UserFactory


class BaseTestCase(TestCase):
    """
    テストの基本クラス
    必須のデータを登録
    """
    fixtures = []


class AuthViewsTestCase(TestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def login(self, email='customer', password='password'):
        return self.client.force_login(self.user)

    def logout(self):
        return self.client.logout()


class ModelsTestCase(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        pass
