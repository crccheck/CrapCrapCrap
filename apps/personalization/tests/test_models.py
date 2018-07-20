from django.test import TestCase

from apps.tracker.factories import ProductFactory
from ..factories import ListFactory
from ..models import pkgen, ListItem


class PkgenTests(TestCase):
    def test_uses_length(self):
        self.assertEqual(len(pkgen(9)), 9)


class ListTests(TestCase):
    def test_flow(self):
        """DELETEME just experimenting"""
        lis = ListFactory()
        product = ProductFactory()

        ListItem.objects.create(product=product, list=lis)
        ListItem.objects.create(product=ProductFactory(), list=lis)

        self.assertEqual(product.lists.count(), 1)
        self.assertEqual(lis.products.count(), 2)
        self.assertEqual(lis.owner.lists.count(), 1)
