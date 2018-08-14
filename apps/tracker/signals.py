import datetime as dt

from django.utils.timezone import now
from django.db.models import Count, Max, Q  # noqa F401
from django.dispatch import Signal

from apps.tracker.models import TrackPoint


# WISHLIST make this async so it doesn't block views.ReceiverView
# or make it a feature and use the it in the response as user feedback
def update_product_pricing(sender, point: TrackPoint, **kwargs):
    """
    Denormalize `Product` pricing when a new `TrackPoint` is added
    """
    week_ago = now() - dt.timedelta(days=7, minutes=1)
    if point.timestamp < week_ago:
        return

    product = point.product
    point.refresh_from_db()  # make sure `price` isn't a str
    week_prices = []
    day_prices = []
    one_day_ago = now() - dt.timedelta(days=1, minutes=1)
    for x in product.prices.filter(timestamp__gte=week_ago):
        week_prices.append(x.price)
        if x.timestamp > one_day_ago:
            day_prices.append(x.price)
    # TODO do this in the database instead of Python
    # max_week = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=70, minutes=1)))
    # max_day = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=2, minutes=1)))
    # out = product.prices.aggregate(
    #     count=Count('id'),
    #     max_week=max_week,
    #     week_diff=max_week - point.price,
    #     day_diff=max_day - point.price,
    # )
    min_prices = [product.min_price] + week_prices
    min_prices = [x for x in min_prices if x]
    product.min_price = min(min_prices)

    product.last_price = point.price
    product.last_price_check = point.timestamp

    if day_prices:
        product.price_drop_short = max(day_prices) - point.price
    else:
        product.price_drop_short = 0
    product.price_drop_long = max(week_prices) - point.price

    price_bases = [product.last_price] + week_prices
    price_bases = [x for x in price_bases if x]
    product.price_base = max(price_bases)

    product.save()


track_point_added = Signal(providing_args=['product'])
track_point_added.connect(update_product_pricing)
