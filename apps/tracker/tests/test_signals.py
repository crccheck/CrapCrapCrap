import datetime as dt
from random import shuffle

from django.test import TestCase
from django.utils import timezone

from ..factories import ProductFactory, TrackPointFactory
from ..signals import track_point_added


class TrackPointTests(TestCase):
    def test_old_track_point_adds_nothing(self):
        point = TrackPointFactory(
            timestamp=timezone.now() - dt.timedelta(days=8),
            price='10',
        )
        track_point_added.send(sender=self, point=point)

        self.assertEqual(point.product.last_price, None)

    def test_pricing_information_is_added_to_product(self):
        product = ProductFactory()
        prices = list(range(1000, 1070, 10))
        beginning = timezone.now() - dt.timedelta(days=len(prices))
        shuffle(prices)
        for idx, x in enumerate(prices):
            point = TrackPointFactory(
                product=product,
                timestamp=beginning + dt.timedelta(days=idx),
                price=x,
            )
            track_point_added.send(sender=self, point=point)

        self.assertEqual(product.price_base, 1080)
        self.assertEqual(product.min_price, 1000)
        self.assertEqual(product.last_price, point.price)
        self.assertEqual(product.price_drop_day, 10)
        self.assertEqual(product.price_drop_week, 70)
