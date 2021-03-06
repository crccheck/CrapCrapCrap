import json

from django.test import Client, TestCase
from django.urls import reverse

from apps.tracker.factories import ProductFactory
from ..factories import ListFactory, UserFactory
from ..models import ListItem


class ListDetailTests(TestCase):
    url = reverse('wishlist-detail')

    def setUp(self):
        self.client = Client()
        self.product = ProductFactory()
        self.lis = ListFactory()
        ListItem.objects.create(list=self.lis, product=self.product)
        self.client.force_login(self.lis.owner)

    def test_returns_list_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.json()['wishlist'], [self.product.key])


class ListToggleTests(TestCase):
    url = reverse('wishlist-toggle')

    def setUp(self):
        self.client = Client()
        self.product = ProductFactory()
        self.user = UserFactory()
        self.client.force_login(self.user)

    # PUT
    #####

    def test_adds_product_to_list(self):
        lis = ListFactory(owner=self.user)

        response = self.client.put(
            self.url,
            data=json.dumps({'products': [self.product.key]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, lis.products.all())
        self.assertTrue(response.json()[self.product.key])

    def test_existing_product_to_list_is_noop(self):
        lis = ListFactory(owner=self.user)
        ListItem.objects.create(list=lis, product=self.product)

        response = self.client.put(
            self.url,
            data=json.dumps({'products': [self.product.key]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, lis.products.all())

    def test_list_is_created_if_user_has_none(self):
        response = self.client.put(
            self.url,
            data=json.dumps({'products': [self.product.key]}),
            content_type='application/json')

        self.assertEqual(self.user.lists.count(), 1)
        lis = self.user.lists.get()
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, lis.products.all())

    # DELETE
    ########

    def test_deletes_nothing_from_empty_list(self):
        lis = ListFactory(owner=self.user)

        response = self.client.delete(
            self.url,
            data=json.dumps({'products': [self.product.key]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.product, lis.products.all())

    def test_deletes_product_from_empty_list(self):
        lis = ListFactory(owner=self.user)
        ListItem.objects.create(list=lis, product=self.product)

        response = self.client.delete(
            self.url,
            data=json.dumps({'products': [self.product.key]}),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.product, lis.products.all())
