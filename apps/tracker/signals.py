from django.dispatch import Signal


track_point_added = Signal(providing_args=['product'])


def update_product_pricing(sender, product, **kwargs):
    print('update_product_pricing', sender, product, kwargs)


track_point_added.connect(update_product_pricing)
