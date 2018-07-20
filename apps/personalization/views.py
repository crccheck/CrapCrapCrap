import json

from django.http import HttpResponse
from django.views import View

from apps.personalization.models import List, ListItem
from apps.tracker.models import Product


class ListToggle(View):
    def put(self, request):
        data = json.loads(request.body)
        products_to_add = Product.objects.filter(pk__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        for product in products_to_add:
            ListItem.objects.get_or_create(list=lis, product=product)

        return HttpResponse(json.dumps({}), content_type='application/json')

    def delete(self, request):
        data = json.loads(request.body)
        products_to_del = Product.objects.filter(pk__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        for product in products_to_del:
            r = ListItem.objects.filter(list=lis, product=product).delete()
            print(r)

        return HttpResponse(json.dumps({}), content_type='application/json')
