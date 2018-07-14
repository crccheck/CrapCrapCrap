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

        self.assertEqual(response.status_code, 204)
        property = Property.objects.get(url='www.bbts.local')
        product = Product.objects.get(property=property, identifier='77021')
        self.assertEqual(product.prices.count(), 1)

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

        self.assertEqual(response.status_code, 204)
        property = Property.objects.get(url='www.bbts.local')
        product = Product.objects.get(property=property, identifier='77021')
        self.assertEqual(product.prices.count(), 2)
