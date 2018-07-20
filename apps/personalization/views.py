import json

from django.http import JsonResponse
from django.views import View

from apps.personalization.models import List, ListItem
from apps.tracker.models import Product


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
            'list': list(lis.products.all().values_list('pk', flat=True)),
        })


class ListToggle(View):
    def put(self, request):
        data = json.loads(request.body)
        products_to_add = Product.objects.filter(pk__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        ret = {}
        for product in products_to_add:
            ListItem.objects.get_or_create(list=lis, product=product)
            ret[product.pk] = True

        return JsonResponse(ret)

    def delete(self, request):
        data = json.loads(request.body)
        products_to_del = Product.objects.filter(pk__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        ret = {}
        for product in products_to_del:
            count, __ = ListItem.objects.filter(list=lis, product=product).delete()
            ret[product.pk] = count

        return JsonResponse(ret)
