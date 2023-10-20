import factory
from factory.django import DjangoModelFactory

from yoka.contacts.models import Contact, ContactStatus


class ContactStatusFactory(DjangoModelFactory):
    class Meta:
        model = ContactStatus

    name = factory.Sequence(lambda n: 'ステータス_%d' % n)
    rank = factory.Sequence(lambda n: n)


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    subject = factory.Sequence(lambda n: '件名_%d' % n)
    message = factory.Faker('text')
    email = factory.Faker('email')
