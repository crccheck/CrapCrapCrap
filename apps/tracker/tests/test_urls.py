from django.test import Client, TestCase
from apps.tracker.models import Property, Product

POINT_DATA = '{"referrer":"https://www.bbts.local/Product/VariationDetails/77021","data":[{"name":"Marvel LS-022SP Iron Man Mark 43 Pewter Finish Special Edition (LE 30)","identifier":"77021","url":"https://www.bbts.local/Product/VariationDetails/77021","price":"19999.99"}],"v":1}'  # noqa


class ReceiverTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_creates_property(self):
        response = self.client.post(
            '/receive/',
            content_type='application/json',
            data=POINT_DATA,
        )

        self.assertEqual(response.status_code, 200)
        property = Property.objects.get(url='www.bbts.local')
        product = Product.objects.get(property=property, identifier='77021')
        self.assertEqual(product.prices.count(), 1)

    def test_property_search_is_loose(self):
        call_1 = '{"referrer":"https://www.bbts.local/Product/VariationDetails/77021","data":[],"v":1}'  # noqa
        call_2 = '{"referrer":"http://bbts.local/Product/VariationDetails/77021","data":[],"v":1}'  # noqa
        response = self.client.post(
            '/receive/',
            content_type='application/json',
            data=call_1,
        )
        response = self.client.post(
            '/receive/',
            content_type='application/json',
            data=call_2,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Property.objects.count(), 1)
        property = Property.objects.get(url='www.bbts.local')
        self.assertTrue(property)

    def test_repeated_post_works(self):
        response = self.client.post(
            '/receive/',
            content_type='application/json',
            data=POINT_DATA,
        )
        response = self.client.post(
            '/receive/',
            content_type='application/json',
            data=POINT_DATA,
        )

        self.assertEqual(response.status_code, 200)
        property = Property.objects.get(url='www.bbts.local')
        product = Product.objects.get(property=property, identifier='77021')
        self.assertEqual(product.prices.count(), 2)
