import datetime as dt
import random

from django.db.models import Min, F, Window
from django.db.models.functions import ExtractWeek
from django.test import TestCase
from django.utils import timezone

from ..factories import ProductFactory, TrackPointFactory
from ..models import TrackPoint


class TrackPointTests(TestCase):
    def test_window_functions_can_find_price_drops(self):
        product = ProductFactory()
        # factory_boy doesn't support bulk_create :(
        for x in range(0, 100, 5):
            TrackPointFactory(
                product=product,
                timestamp=timezone.now() - dt.timedelta(days=x),
                price=random.randint(100, 999),
            )

        qs = TrackPoint.objects.annotate(
            min_price=Window(
                expression=Min('price'),
                partition_by=[F('product')],
                order_by=ExtractWeek('timestamp').asc(),
            ),
            price_drop=F('price') - F('min_price'),
        ).order_by('-price_drop')
        # for x in qs:
        #     print(x, x.price, x.min_price, x.price_drop)
