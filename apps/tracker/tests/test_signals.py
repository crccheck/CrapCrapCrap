import datetime as dt

from django.test import TestCase
from django.utils import timezone

from ..factories import ProductFactory, TrackPointFactory
from ..signals import track_point_added


class TrackPointTests(TestCase):
    def test_window_functions_can_find_price_drops(self):
        product = ProductFactory()
        for x in range(0, 10):
            now = timezone.now()
            TrackPointFactory(
                product=product,
                timestamp=now - dt.timedelta(days=x),
                price=1000 + 10 * x,
            )

        track_point_added.send(sender=self, product=product)
        self.assertEqual(product.last_price, 1000)
        self.assertEqual(product.price_drop_day, 10)
        self.assertEqual(product.price_drop_week, 70)
