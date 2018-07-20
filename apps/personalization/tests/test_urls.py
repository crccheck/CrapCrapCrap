import json

from django.test import Client, TestCase
from django.urls import reverse

from apps.tracker.factories import ProductFactory
from ..factories import ListFactory


class ListToggleTests(TestCase):
    url = reverse('list-toggle')

    def setUp(self):
        self.client = Client()

    def test_response(self):
        lis = ListFactory()
        product = ProductFactory()
        self.client.force_login(lis.owner)

        response = self.client.post(
            self.url,
            data=json.dumps({'products': [product.pk]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(product, lis.products.all())
