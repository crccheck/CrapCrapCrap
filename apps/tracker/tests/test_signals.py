import datetime as dt

from django.test import TestCase
from django.utils import timezone

from ..factories import ProductFactory, TrackPointFactory
from ..signals import track_point_added


class TrackPointTests(TestCase):
    def test_pricing_information_is_added_to_product(self):
        product = ProductFactory()
        now = timezone.now()
        for x in range(0, 10):
            TrackPointFactory(
                product=product,
                timestamp=now - dt.timedelta(days=x),
                price=1000 + 10 * x,
            )

        track_point_added.send(sender=self, product=product)

        self.assertEqual(product.last_price, 1000)
        self.assertEqual(product.last_price_check, now)
        self.assertEqual(product.price_drop_day, 10)
        self.assertEqual(product.price_drop_week, 70)
