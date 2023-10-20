import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.django.Password('a9XT7Kqb')
    email = factory.Faker('email')

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class SuperUserFactory(UserFactory):
    """管理者"""
    is_superuser = True
    is_staff = True


class StaffFactory(UserFactory):
    """スタッフ"""
    is_staff = True


class AnonymousUserFactory(factory.Factory):
    """匿名ユーザー"""

    class Meta:
        model = AnonymousUser
