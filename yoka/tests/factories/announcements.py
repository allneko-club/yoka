import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from yoka.announcements.models import Announcement
from .users import StaffFactory


class AnnouncementFactory(DjangoModelFactory):
    class Meta:
        model = Announcement

    title = factory.Sequence(lambda n: 'タイトル%d' % n)
    content = factory.Sequence(lambda n: '内容%d' % n)
    update_user = SubFactory(StaffFactory)
    create_user = SubFactory(StaffFactory)
