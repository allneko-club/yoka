from yoka.tests.factories import *
from yoka.tests.utils.views import ModelsTestCase
from yoka.users.models import Address


class TestAddress(ModelsTestCase):
    fixtures = ["address"]

    def test_ordering(self):
        addresses = Address.objects.all()
        self.assertTrue(addresses[0].rank < addresses[1].rank)


class TestUser(ModelsTestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_get_absolute_url(self):
        assert self.user.get_absolute_url() == f"/user/{self.user.id}/"
