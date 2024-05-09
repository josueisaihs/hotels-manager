from django.test import TestCase
from django.urls import reverse


class TestSettings(TestCase):
    def test_autodoc_pages(self):
        response = self.client.get(reverse("schema-swagger-ui"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("schema-redoc"))
        self.assertEqual(response.status_code, 200)
