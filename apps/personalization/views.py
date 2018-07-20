import json

from django.http import HttpResponse
from django.views import View

from apps.tracker.models import Product


class ListToggle(View):
    def post(self, request):
        # if not request.is_ajax():
        #     return HttpResponseBadRequest()

        data = json.loads(request.body)
        products_to_add = Product.objects.filter(pk__in=data['products'])
        print(products_to_add)
        return HttpResponse()
