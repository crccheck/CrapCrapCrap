from django.test import TestCase

from ..factories import UserFactory


class ListTests(TestCase):
    def test_factory(self):
        user = UserFactory()
        print(user)
