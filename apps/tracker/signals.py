import datetime as dt

from django.utils.timezone import now
from django.db.models import Count, Max, Min, Q  # noqa F401
from django.dispatch import Signal

from apps.tracker.models import TrackPoint


# WISHLIST make this async so it doesn't block views.ReceiverView
# or make it a feature and use the it in the response as user feedback
def update_product_pricing(sender, point: TrackPoint, **kwargs) -> None:
    """
    Denormalize `Product` pricing when a new `TrackPoint` is added
    """
    week_ago = now() - dt.timedelta(days=7, minutes=1)
    if point.timestamp < week_ago:
        return

    product = point.product
    point.refresh_from_db()  # make sure `price` isn't a str

    week_prices = product.prices.filter(timestamp__gte=week_ago).values_list('price', flat=True)
    print(week_prices)
    product.price_drop_short = max(week_prices) - point.price

    max_ever = Max('price')
    min_ever = Min('price')
    all_price_info = product.prices.aggregate(
        count=Count('id'),
        max_ever=max_ever,
        min_ever=min_ever,
    )
    product.price_base = all_price_info["max_ever"]
    product.min_price = all_price_info["min_ever"]
    product.price_drop_long = product.price_base - point.price
    product.last_price = point.price
    product.last_price_check = point.timestamp

    product.save()


track_point_added = Signal(providing_args=['point'])
track_point_added.connect(update_product_pricing)
