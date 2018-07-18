import json
import logging
import re
from urllib.parse import urlparse

from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse

from apps.tracker.models import Property, Product, TrackPoint


logger = logging.getLogger(__name__)


class ReceiverView(View):
    def post(self, request):
        logger.debug(request.body)
        try:
            data = json.loads(request.body)
        except ValueError as e:
            return HttpResponse(status=400)

        hostname = urlparse(data['referrer']).hostname
        base_url = re.match(r'(www.)?(.*)', hostname).groups()[1]
        try:
            property = Property.objects.get(url__icontains=base_url)
        except Property.DoesNotExist:
            property = Property.objects.create(name=base_url, url=hostname)

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


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')[:10]
        return context
