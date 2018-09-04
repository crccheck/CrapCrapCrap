import json
import logging
import re
from urllib.parse import urlparse
from typing import List, Union

from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponse, JsonResponse

from .models import Property, Product, TrackPoint
from .signals import track_point_added


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
        for point in TrackPoint.objects.bulk_create(points):
            track_point_added.send(sender=self, point=point)

        crap_host = request.META.get("HTTP_HOST")
        pks = ','.join([str(x.product.pk) for x in points])
        ret = {
            'search_url': f'{request.scheme}://{crap_host}/search?products={pks}',
            'deal_found': False,  # TODO
        }
        return JsonResponse(data=ret, status=200)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = (
            Product.objects.filter(last_price_check__isnull=False)
            .select_related('property')
            .order_by('-last_price_check')[:20])
        return context


class SearchList(ListView):
    context_object_name = 'products'
    model = Product
    paginate_by = 100
    template_name = 'search.html'

    def get_queryset(self) -> Union[QuerySet, List]:
        qs = super().get_queryset().order_by('price_drop_long').select_related('property')
        query = self.request.GET.get('q')
        if query:
            return qs.filter(name__icontains=query)

        products = self.request.GET.get('products')
        if products:
            # NOTE: this path will return a list instead of a queryset
            product_pks = list(map(int, products.split(',')))
            object_list = list(qs.filter(pk__in=product_pks))
            object_list.sort(key=lambda x: product_pks.index(x.pk))
            return object_list

        # TODO handle no query case
        return qs[:100]


class ProductDetail(DetailView):
    model = Product

    def get_queryset(self):
        return super().get_queryset().select_related('property')
