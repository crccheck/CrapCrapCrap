from django.test import TestCase

from ..factories import TrackPointFactory


class TrackPointTests(TestCase):
    def test_works(self):
        TrackPointFactory()
