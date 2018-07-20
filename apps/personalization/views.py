import json

from django.http import HttpResponse
from django.views import View

from apps.personalization.models import List, ListItem
from apps.tracker.models import Product


class ListToggle(View):
    def post(self, request):
        # if not request.is_ajax():
        #     return HttpResponseBadRequest()

        data = json.loads(request.body)
        products_to_add = Product.objects.filter(pk__in=data['products'])

        try:
            lis = request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = request.user.lists.create(name='Wishlist')

        for product in products_to_add:
            ListItem.objects.create(list=lis, product=product)

        return HttpResponse(json.dumps({}), content_type='application/json')
