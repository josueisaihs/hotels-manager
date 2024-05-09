from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework.test import APITestCase

from app.hotels.models import Hotel, HotelChain
from ..base import image_path, User


class TestSetup(APITestCase):
    def setUp(self):
        user = {"email": "test@test.com", "password": "foo"}
        User.objects.create_reviewer(**user)  # type: ignore

        response = self.client.post(reverse("token_obtain_pair"), user, format="json")
        token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")  # type: ignore

        self.flatten_chain_data = lambda x: {f"chain.{k}": v for k, v in x.items()}

        self.image_path = image_path

        self.special_chains = ["test chain", "special chain", "unique chain"]

        HotelChain.objects.create(
            title=self.special_chains[0],
        )

        with open(self.image_path, "rb") as f:
            Hotel.objects.create(
                name="test hotel",
                location="test city",
                slug="test-hotel-test-land",
                photo=SimpleUploadedFile("test.png", f.read(), "image/png"),
            )

            Hotel.objects.create(
                name="test resort",
                location="somewhere",
                slug="test-resort-somewhere",
                photo=SimpleUploadedFile("test.png", f.read(), "image/png"),
            )
