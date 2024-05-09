from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

User = get_user_model()


class JwtTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example@example.com", password="foo"
        )

    def test_jwt(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": "foo"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
