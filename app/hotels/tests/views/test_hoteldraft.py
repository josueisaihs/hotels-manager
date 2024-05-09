from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings

from rest_framework import status

from app.hotels.models import Hotel, HotelDraft
from ..base import User, TEST_LOCATION
from .base import TestSetup


# region HotelDraftView Auth
class HotelDraftViewSetTestCase(TestSetup):
    """
    Test cases for HotelDraftViewSet API with authentication
    """

    def setUp(self):
        super().setUp()

        self.isReadOnly = (
            settings.REST_FRAMEWORK.get("DEFAULT_PERMISSION_CLASSES")[0]
            == "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        )

        self.hotel_slug = Hotel.objects.get(name="test hotel").slug

    def test_get_list(self):
        HotelDraft.objects.create(
            hotel=Hotel.objects.get(name="test hotel"),
            name="test draft",
            location="test city",
            photo=Hotel.objects.get(name="test hotel").photo,
            created_by=User.objects.first(),
        )
        HotelDraft.objects.create(
            hotel=Hotel.objects.get(name="test resort"),
            name="test draft 2",
            location="test city",
            photo=Hotel.objects.get(name="test resort").photo,
            created_by=User.objects.first(),
        )

        url = reverse("hoteldraft-list")
        response = self.client.get(url)

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("count")
        expected = 2
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results").__len__()
        self.assertEqual(result, 2, msg=response.json())

    def test_create(self):
        url = reverse("hoteldraft-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        with open(self.image_path, "rb") as f:
            data = {
                "hotel": self.hotel_slug,
                "name": f"new hotel {chain_title}",
                "location": TEST_LOCATION[0][0],
                "photo": SimpleUploadedFile("test.png", f.read(), "image/png"),
            }
            data.update(self.flatten_chain_data(chain_data))

            response = self.client.post(url, data, format="multipart")

            result = response.json().get("name")
            expected = data["name"]
            self.assertEqual(result, expected, msg=response.json())

            result = response.json().get("chain").get("title")
            self.assertEqual(result, chain_title.title(), msg=response.json())

            result = response.status_code
            expected = status.HTTP_201_CREATED
            self.assertEqual(result, expected, msg=response.json())

    def test_update(self):
        hotel = Hotel.objects.get(name="test hotel")
        draft = HotelDraft.objects.create(
            hotel=hotel,
            name="test draft",
            location=TEST_LOCATION[0][0],
            photo=hotel.photo,
            created_by=User.objects.first(),
        )
        url = reverse("hoteldraft-detail", kwargs={"slug": draft.slug})

        data = {
            "hotel": hotel.slug,
            "name": "updated hotel",
            "location": TEST_LOCATION[1][0],
        }

        response = self.client.patch(url, data, format="json")

        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("name")
        expected = data["name"]
        self.assertEqual(result, expected, msg=response.json())

    def test_delete(self):
        hotel_name = "test hotel"

        hotel = Hotel.objects.get(name=hotel_name)
        draft = HotelDraft.objects.create(
            hotel=hotel,
            name="test draft",
            location="test city",
            photo=hotel.photo,
            created_by=User.objects.first(),
        )
        url = reverse("hoteldraft-detail", kwargs={"slug": draft.slug})

        response = self.client.delete(url)

        result = response.status_code
        expected = status.HTTP_204_NO_CONTENT
        self.assertEqual(result, expected)


# region HotelDraftView NoAuth
class HotelDraftViewSetNoAuthTestCase(TestSetup):
    """
    Test cases for HotelDraftViewSet API without authentication
    """

    def setUp(self):
        super().setUp()

        self.isReadOnly = (
            settings.REST_FRAMEWORK.get("DEFAULT_PERMISSION_CLASSES")[0]
            == "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        )

        self.hotel_slug = Hotel.objects.get(name="test hotel").slug

        # remove authentication
        self.client.credentials()  # type: ignore

    def test_get_list(self):
        """
        Test get list without authentication

        If isReadOnly is True, Expected: 200
        If isReadOnly is False, Expected: 401
        """
        url = reverse("hoteldraft-list")
        response = self.client.get(url)

        result = response.status_code
        expected = (
            status.HTTP_200_OK if self.isReadOnly else status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(result, expected, msg=response.json())

        if self.isReadOnly:
            result = response.json().get("count")
            expected = 0
            self.assertEqual(result, expected, msg=response.json())
        else:
            result = response.json().get("detail")
            expected = "Authentication credentials were not provided."
            self.assertEqual(result, expected, msg=response.json())

    def test_create(self):
        """
        Test create without authentication

        Expected: 401
        """
        url = reverse("hoteldraft-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        with open(self.image_path, "rb") as f:
            data = {
                "hotel": self.hotel_slug,
                "name": f"new hotel {chain_title}",
                "location": TEST_LOCATION[1][0],
                "photo": SimpleUploadedFile("test.png", f.read(), "image/png"),
            }
            data.update(self.flatten_chain_data(chain_data))

            response = self.client.post(url, data, format="multipart")

            result = response.status_code
            expected = status.HTTP_401_UNAUTHORIZED
            self.assertEqual(result, expected, msg=response.json())
