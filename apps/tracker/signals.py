import datetime as dt

from django.utils.timezone import now
from django.db.models import Max, Q
from django.dispatch import Signal


track_point_added = Signal(providing_args=['product'])


def update_product_pricing(sender, product, **kwargs):
    latest_track = product.prices.latest('timestamp')
    max_week = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=7, minutes=1)))
    max_day = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=1, minutes=1)))
    out = product.prices.aggregate(
        week_diff=max_week - latest_track.price,
        day_diff=max_day - latest_track.price,
    )
    product.last_price = latest_track.price
    product.price_drop_day = out['day_diff']
    product.price_drop_week = out['week_diff']
    product.save()


track_point_added.connect(update_product_pricing)