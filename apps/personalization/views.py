import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from apps.personalization.models import List, ListItem
from apps.tracker.models import Product


class SearchList(TemplateView):
    template_name = 'search.html'


class WishlistDetail(View):
    """
    This might morph into a view that returns all the user state necessary.
    """
    def get(self, request):
        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        return JsonResponse({
            'wishlist': list(lis.products.all().values_list('key', flat=True)),
        })


class ListToggle(View):
    def put(self, request):
        data = json.loads(request.body)
        products_to_add = Product.objects.filter(key__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        ret = {}
        for product in products_to_add:
            ListItem.objects.get_or_create(list=lis, product=product)
            ret[product.key] = True

        return JsonResponse(ret)

    def delete(self, request):
        data = json.loads(request.body)
        products_to_del = Product.objects.filter(key__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        ret = {}
        for product in products_to_del:
            count, __ = ListItem.objects.filter(list=lis, product=product).delete()
            ret[product.key] = count

        return JsonResponse(ret)
