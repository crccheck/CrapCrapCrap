from django.test import TestCase

from ..factories import UserFactory, ListFactory


class ListTests(TestCase):
    def test_factory(self):
        lis = ListFactory()
        print('list', lis, lis.pk)
