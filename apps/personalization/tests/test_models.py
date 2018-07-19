from django.test import TestCase

from apps.tracker.factories import ProductFactory
from ..factories import UserFactory, ListFactory
from ..models import ListItem


class ListTests(TestCase):
    def test_factory(self):
        lis = ListFactory()
        print('list', lis, lis.pk)
        product = ProductFactory()
        ListItem.objects.create(product=product, list=lis)
        print(product.lists.all())
