from django.conf import settings
from django.urls import reverse

from rest_framework import status

from app.hotels.models import HotelChain
from ..base import User
from .base import TestSetup


# region HotelChainView Auth
class HotelChainViewSetTestCase(TestSetup):
    def setUp(self):
        super().setUp()

    def test_get_list(self):
        url = reverse("hotelchain-list")
        response = self.client.get(url)

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("count")
        expected = 1
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results").__len__()
        self.assertEqual(result, 1, msg=response.json())

    def test_get_detail(self):
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})
        response = self.client.get(url)

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("title")
        expected = self.special_chains[0].title()
        self.assertEqual(result, expected, msg=response.json())

    def test_create(self):
        url = reverse("hotelchain-list")

        data = {
            "title": "new chain",
        }

        response = self.client.post(url, data, format="json")

        result = response.json().get("title")
        expected = data["title"].title()
        self.assertEqual(result, expected, msg=response.json())

        result = response.status_code
        expected = status.HTTP_201_CREATED
        self.assertEqual(result, expected, msg=response.json())

    def test_update(self):
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})

        data = {
            "title": "updated chain",
            "price_range": 4,
        }

        response = self.client.patch(url, data, format="json")

        result = response.json().get("title")
        expected = data["title"].title()
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("price_range")
        expected = data["price_range"]
        self.assertEqual(result, expected, msg=response.json())

        result = chain.price_range
        expected = data["price_range"]
        self.assertNotEqual(result, expected, msg=response.json())

        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(result, expected, msg=response.json())

    def test_delete(self):
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})

        response = self.client.delete(url)

        result = response.status_code
        expected = status.HTTP_204_NO_CONTENT
        self.assertEqual(result, expected)

        url = reverse("hotelchain-list")
        response = self.client.get(url)

        result = response.json().get("count")
        expected = 0
        self.assertEqual(result, expected, msg=response.json())

    def test_create_with_invalid_title(self):
        url = reverse("hotelchain-list")

        data = {
            "title": "",
        }

        response = self.client.post(url, data, format="json")

        result = response.status_code
        expected = status.HTTP_400_BAD_REQUEST
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("title")
        expected = ["This field may not be blank."]
        self.assertEqual(result, expected, msg=response.json())

    def test_create_with_existing_title(self):
        url = reverse("hotelchain-list")

        data = {
            "title": self.special_chains[0].upper(),
        }

        response = self.client.post(url, data, format="json")

        result = response.status_code
        expected = status.HTTP_201_CREATED
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("title")
        expected = ["Hotel Chain with this Title already exists."]
        self.assertNotEqual(result, expected, msg=response.json())

        result = response.json().get("title")
        expected = self.special_chains[0].title().title()
        self.assertEqual(result, expected, msg=response.json())

    def test_create_without_title(self):
        url = reverse("hotelchain-list")

        response = self.client.post(url, {}, format="json")

        result = response.status_code
        expected = status.HTTP_400_BAD_REQUEST
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("title")
        expected = ["This field is required."]
        self.assertEqual(result, expected, msg=response.json())


# region HotelChainView NoAuth
class HotelChainViewSetNoAuthTestCase(TestSetup):
    """
    Test cases for HotelChainViewSet API without authentication
    """

    def setUp(self):
        super().setUp()

        self.isReadOnly = (
            settings.REST_FRAMEWORK.get("DEFAULT_PERMISSION_CLASSES")[0]
            == "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        )

        # remove authentication
        self.client.credentials()  # type: ignore

    def test_get_list(self):
        """
        Test get list without authentication

        If isReadOnly is True, Expected: 200
        If isReadOnly is False, Expected: 401
        """
        url = reverse("hotelchain-list")
        response = self.client.get(url)

        result = response.status_code
        expected = (
            status.HTTP_200_OK if self.isReadOnly else status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(result, expected, msg=response.json())

        if self.isReadOnly:
            result = response.json().get("count")
            expected = 1
            self.assertEqual(result, expected, msg=response.json())
        else:
            result = response.json().get("detail")
            expected = "Authentication credentials were not provided."
            self.assertEqual(result, expected, msg=response.json())

    def test_get_detail(self):
        """
        Test get detail without authentication

        If isReadOnly is True, Expected: 200
        If isReadOnly is False, Expected: 401
        """
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})
        response = self.client.get(url)

        result = response.status_code
        expected = (
            status.HTTP_200_OK if self.isReadOnly else status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(result, expected, msg=response.json())

        if self.isReadOnly:
            result = response.json().get("title")
            expected = self.special_chains[0].title()
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
        url = reverse("hotelchain-list")

        data = {
            "title": "new chain",
        }

        response = self.client.post(url, data, format="json")

        result = response.status_code
        expected = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(result, expected, msg=response.json())

    def test_update(self):
        """
        Test update without authentication

        Expected: 401
        """
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})

        data = {
            "title": "updated chain",
        }

        response = self.client.patch(url, data, format="json")

        result = response.status_code
        expected = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(result, expected)

    def test_delete(self):
        """
        Test delete without authentication

        Expected: 401
        """
        chain = HotelChain.objects.get(title__iexact=self.special_chains[0])
        url = reverse("hotelchain-detail", kwargs={"slug": chain.slug})

        response = self.client.delete(url)

        result = response.status_code
        expected = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(result, expected)
