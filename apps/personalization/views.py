import json

from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.personalization.models import List, ListItem
from apps.tracker.models import Product


class Logout(View):
    def post(self, request):
        if request.user.is_anonymous:
            return HttpResponseBadRequest()

        logout(request)
        return HttpResponseRedirect(reverse('home'))


class Profile(TemplateView):
    template_name = 'profile.html'


class WishlistDetail(ListView):
    model = ListItem
    paginate_by = 100
    template_name = 'wishlist.html'

    def get_queryset(self):
        try:
            lis = self.request.user.lists.earliest('created')
        except List.DoesNotExist:
            lis = self.request.user.lists.create(name='Wishlist')

        qs = super().get_queryset()
        return qs.filter(list=lis)


class ApiWishlistDetail(View):
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
