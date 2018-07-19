import factory
from django.conf import settings

from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL


class ListFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.List
    name = 'Wishlist'
    owner = factory.SubFactory(UserFactory)
