import datetime as dt

from django.utils.timezone import now
from django.db.models import Max, Q
from django.dispatch import Signal


track_point_added = Signal(providing_args=['product'])


def update_product_pricing(sender, product, **kwargs):
    latest_track = product.prices.latest('timestamp')
    max_week = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=7)))
    max_day = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=1)))
    out = product.prices.aggregate(
        week_diff=max_week - latest_track.price,
        day_diff=max_day - latest_track.price,
    )
    print('update_product_pricing', latest_track, out)


track_point_added.connect(update_product_pricing)
