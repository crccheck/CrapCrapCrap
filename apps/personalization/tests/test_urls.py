from django.test import Client, TestCase
from django.urls import reverse

from ..factories import ListFactory


class ListToggleTests(TestCase):
    url = reverse('list-toggle')

    def setUp(self):
        self.client = Client()

    def test_response(self):
        lis = ListFactory()
        self.client.force_login(lis.owner)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
