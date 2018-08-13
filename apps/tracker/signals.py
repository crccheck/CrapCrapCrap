import datetime as dt

from django.utils.timezone import now
from django.db.models import Count, Max, Q
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
    points = product.prices.filter(timestamp__gte=now() - dt.timedelta(days=7, minutes=1))
    print([x.timestamp for x in product.prices.all()])
    week_prices = []
    one_day_ago = now() - dt.timedelta(days=1, minutes=1)
    day_prices = []
    for x in points:
        week_prices.append(x.price)
        if x.timestamp > one_day_ago:
            day_prices.append(x.price)
    # print(week_prices)
    # max_week = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=70, minutes=1)))
    # max_day = Max('price', filter=Q(timestamp__gte=now() - dt.timedelta(days=2, minutes=1)))
    # out = product.prices.aggregate(
    #     count=Count('id'),
    #     max_week=max_week,
    #     week_diff=max_week - point.price,
    #     day_diff=max_day - point.price,
    # )
    min_prices = [product.min_price, point.price] + week_prices
    print(min_prices)
    min_prices = [x for x in min_prices if x]

    product.min_price = min(min_prices)
    product.last_price = point.price
    product.last_price_check = point.timestamp
    product.price_drop_day = out['day_diff']
    product.price_drop_week = out['week_diff']
    price_bases = [product.last_price, out['max_week']]
    price_bases = [x for x in price_bases if x]
    product.price_base = max(price_bases)
    product.save()


track_point_added = Signal(providing_args=['product'])
track_point_added.connect(update_product_pricing)
