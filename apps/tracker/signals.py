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

    all_price_info = product.prices.aggregate(
        # count=Count('id'),
        max_ever=Max('price'),
        min_ever=Min('price'),
    )
    product.price_base = all_price_info["max_ever"]
    product.min_price = all_price_info["min_ever"]
    product.price_drop_long = product.price_base - point.price
    product.last_price = point.price
    product.last_price_check = point.timestamp

    week_price_info = product.prices.filter(timestamp__gte=week_ago).aggregate(
        # count=Count('id'),
        max_week=Max('price'),
    )
    product.price_drop_short = week_price_info["max_week"] - point.price

    product.save()


track_point_added = Signal(providing_args=['point'])
track_point_added.connect(update_product_pricing)
