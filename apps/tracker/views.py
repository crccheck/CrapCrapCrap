import json
from urllib.parse import urlparse

from django.views import View
from django.http import HttpResponse

from apps.tracker.models import Property, Product, TrackPoint


class ReceiverView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except ValueError as e:
            return HttpResponse(status=400)

        property, created = Property.objects.get_or_create(
            url=urlparse(data['referrer']).hostname
        )

        product_ids = [x['identifier'] for x in data['data']]
        known_products = Product.objects.filter(identifier__in=product_ids)
        product_map = {x.identifier: x for x in known_products}
        new_products = Product.objects.bulk_create([
            Product(
                property=property,
                identifier=x['identifier'],
                name=x['name'],
                url=x['url'],
            ) for x in data['data'] if x['identifier'] not in product_map
        ])
        for product in new_products:
            product_map[product.identifier] = product

        points = [
            TrackPoint(
                product=product_map[x['identifier']],
                price=x['price'],
            ) for x in data['data']
        ]
        TrackPoint.objects.bulk_create(points)

        return HttpResponse(status=204)
