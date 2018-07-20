import json

from django.test import Client, TestCase
from django.urls import reverse

from apps.tracker.factories import ProductFactory
from ..factories import ListFactory, UserFactory
from ..models import ListItem


class ListToggleTests(TestCase):
    url = reverse('list-toggle')

    def setUp(self):
        self.client = Client()
        self.product = ProductFactory()

    def test_adds_product_to_list(self):
        lis = ListFactory()
        self.client.force_login(lis.owner)

        response = self.client.post(
            self.url,
            data=json.dumps({'products': [self.product.pk]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, lis.products.all())

    def test_existing_product_to_list_is_noop(self):
        lis = ListFactory()
        product = ProductFactory()
        ListItem.objects.create(list=lis, product=product)
        self.client.force_login(lis.owner)

        response = self.client.post(
            self.url,
            data=json.dumps({'products': [product.pk]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(product, lis.products.all())

    def test_list_is_created_if_user_has_none(self):
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.post(
            self.url,
            data=json.dumps({'products': [self.product.pk]}),
            content_type='application/json')

        self.assertEqual(user.lists.count(), 1)
        lis = user.lists.get()
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, lis.products.all())
