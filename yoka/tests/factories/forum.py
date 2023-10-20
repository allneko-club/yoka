import factory
from factory.django import DjangoModelFactory

from yoka.forum.models import Category, Reply, Thread
from .users import UserFactory


class CategoryFactory(DjangoModelFactory):
    slug = factory.Sequence(lambda n: 'thread_title%d' % n)
    title = factory.Sequence(lambda n: 'thread_title%d' % n)
    description = "category_description"
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Category


class ThreadFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: 'thread_title%d' % n)
    user = factory.SubFactory(UserFactory)
    content = "thread_content"
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Thread


class ReplyFactory(DjangoModelFactory):
    thread = factory.SubFactory(ThreadFactory)
    user = factory.SubFactory(UserFactory)
    content = "post_content"

    class Meta:
        model = Reply
