import datetime as dt

from django.test import TestCase
from django.utils import timezone

from ..factories import ProductFactory, TrackPointFactory
from ..signals import track_point_added


class TrackPointTests(TestCase):
    def test_pricing_information_is_added_to_product(self):
        product = ProductFactory()
        beginning = timezone.now() - dt.timedelta(days=7)
        for x in range(0, 10):
            point = TrackPointFactory(
                product=product,
                timestamp=beginning + dt.timedelta(days=x),
                price=1000 + 10 * x,
            )
            track_point_added.send(sender=self, point=point)

        self.assertEqual(product.price_base, 1090)
        self.assertEqual(product.min_price, 1000)
        self.assertEqual(product.last_price, point.price)
        self.assertEqual(product.price_drop_day, 10)
        self.assertEqual(product.price_drop_week, 70)
