import datetime as dt

from django.utils.timezone import now
from django.db.models import Max, Q
from django.dispatch import Signal


# WISHLIST make this async so it doesn't block views.ReceiverView
# or make it a feature and use the it in the response as user feedback
def update_product_pricing(sender, point, **kwargs):
    """
    Denormalize `Product` pricing when a new `TrackPoint` is added
    """
    product = point.product
    point.refresh_from_db()  # make sure `price` isn't a str
    max_week = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=7, minutes=1)))
    max_day = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=1, minutes=1)))
    out = product.prices.aggregate(
        max_week=max_week,
        week_diff=max_week - point.price,
        day_diff=max_day - point.price,
    )
    min_prices = [product.min_price, product.last_price, point.price]
    min_prices = [x for x in min_prices if x]
    print(out)

    product.min_price = min(min_prices)
    product.last_price = point.price
    product.last_price_check = point.timestamp
    product.price_drop_day = out['day_diff']
    product.price_drop_week = out['week_diff']
    product.price_base = max(product.last_price, out['max_week'])
    product.save()


track_point_added = Signal(providing_args=['product'])
track_point_added.connect(update_product_pricing)
