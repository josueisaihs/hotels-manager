from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings

from rest_framework import status

from app.hotels.models import Hotel, HotelChain
from ..base import TEST_LOCATION
from .base import TestSetup


# region HotelView Auth
class HotelViewSetTestCase(TestSetup):
    """
    Test cases for HotelViewSet API with authentication
    """

    def setUp(self):
        super().setUp()

    def test_get_list(self):
        url = reverse("hotel-list")
        response = self.client.get(url)

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("count")
        expected = 2
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results").__len__()
        self.assertEqual(result, 2, msg=response.json())

    def test_get_list_with_filter_name(self):
        url = reverse("hotel-list")
        filter_value = "resort"
        response = self.client.get(url, {"name": filter_value})

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("count")
        expected = 1
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results").__len__()
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results")[0].get("name")
        expected = "test resort"
        self.assertEqual(result, expected, msg=response.json())

    def test_get_detail(self):
        url = reverse("hotel-detail", kwargs={"slug": "test-hotel-test-land"})
        response = self.client.get(url)

        result = response.status_code
        expected = status.HTTP_200_OK
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("name")
        expected = "test hotel"
        self.assertEqual(result, expected, msg=response.json())

    def test_create(self):
        url = reverse("hotel-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        with open(self.image_path, "rb") as f:
            data = {
                "name": f"new hotel {chain_title}",
                "location": TEST_LOCATION[1][0],
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
        url = reverse("hotel-detail", kwargs={"slug": hotel.slug})

        data = {
            "name": "updated hotel",
            "location": TEST_LOCATION[1][0],
        }

        response = self.client.patch(url, data, format="json")

        result = response.json().get("name")
        expected = data["name"]
        self.assertEqual(result, expected, msg=response.json())

        expected = status.HTTP_200_OK
        result = response.status_code
        self.assertEqual(result, expected, msg=response.json())

    def test_delete(self):
        hotel_name = "test hotel"

        hotel = Hotel.objects.get(name=hotel_name)
        url = reverse("hotel-detail", kwargs={"slug": hotel.slug})

        response = self.client.delete(url)

        result = response.status_code
        expected = status.HTTP_204_NO_CONTENT
        self.assertEqual(result, expected)

        url = reverse("hotel-list")
        response = self.client.get(url)

        result = response.json().get("count")
        expected = 1
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("results")[0].get("name")
        expected = hotel_name
        self.assertNotEqual(result, expected, msg=response.json())

    def test_create_without_chain(self):
        # if chain is required, it should return 400
        url = reverse("hotel-list")

        with open(self.image_path, "rb") as f:
            data = {
                "name": "new hotel",
                "location": TEST_LOCATION[1][0],
                "photo": SimpleUploadedFile("test.png", f.read(), "image/png"),
            }

            response = self.client.post(url, data, format="multipart")

            result = response.status_code
            expected = status.HTTP_400_BAD_REQUEST
            self.assertEqual(result, expected, msg=response.json())

            result = response.json().get("chain")
            expected = ["This field is required."]
            self.assertEqual(result, expected, msg=response.json())

    def test_hotel_with_invalid_chain(self):
        chain_data = {
            "price_range": 1,
            "description": "test description",
            "email": "admin@example.com",
            "phone": "123456789",
            "website": "http://example.com",
            "sales_contact": "test contact",
        }

        data = {
            "name": "test hotel",
            "location": "test location",
        }
        data.update(self.flatten_chain_data(chain_data))

        response = self.client.post(reverse("hotel-list"), data, format="multipart")

        result = response.status_code
        expected = status.HTTP_400_BAD_REQUEST
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("chain").get("title")
        expected = ["This field is required."]
        self.assertEqual(result, expected, msg=response.json())

    def test_create_without_photo(self):
        url = reverse("hotel-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        HotelChain.objects.filter(**chain_data).delete()

        data = {
            "name": f"new hotel {chain_title}",
            "location": TEST_LOCATION[1][0],
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

    def test_create_with_invalid_photo(self):
        url = reverse("hotel-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        data = {
            "name": f"new hotel {chain_title}",
            "location": TEST_LOCATION[1][0],
            "photo": "invalid photo",
        }
        data.update(self.flatten_chain_data(chain_data))

        response = self.client.post(url, data, format="multipart")

        result = response.status_code
        expected = status.HTTP_400_BAD_REQUEST
        self.assertEqual(result, expected, msg=response.json())

        result = response.json().get("photo")
        expected = [
            "The submitted data was not a file. Check the encoding type on the form."
        ]
        self.assertEqual(result, expected, msg=response.json())


# region HotelView NoAuth
class HotelViewSetNoAuthTestCase(TestSetup):
    """
    Test cases for HotelViewSet API with authentication
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
        url = reverse("hotel-list")
        response = self.client.get(url)

        result = response.status_code
        expected = (
            status.HTTP_200_OK if self.isReadOnly else status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(result, expected, msg=response.json())

        if self.isReadOnly:
            result = response.json().get("count")
            expected = 2
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
        url = reverse("hotel-detail", kwargs={"slug": "test-hotel-test-land"})
        response = self.client.get(url)

        result = response.status_code
        expected = (
            status.HTTP_200_OK if self.isReadOnly else status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(result, expected, msg=response.json())

        if self.isReadOnly:
            result = response.json().get("name")
            expected = "test hotel"
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
        url = reverse("hotel-list")

        chain_title = self.special_chains[0]
        chain_data = {
            "title": chain_title,
        }

        with open(self.image_path, "rb") as f:
            data = {
                "name": f"new hotel {chain_title}",
                "location": TEST_LOCATION[1][0],
                "photo": SimpleUploadedFile("test.png", f.read(), "image/png"),
            }
            data.update(self.flatten_chain_data(chain_data))

            response = self.client.post(url, data, format="multipart")

            result = response.status_code
            expected = status.HTTP_401_UNAUTHORIZED
            self.assertEqual(result, expected, msg=response.json())

    def test_update(self):
        """
        Test update without authentication

        Expected: 401
        """
        hotel = Hotel.objects.get(name="test hotel")
        url = reverse("hotel-detail", kwargs={"slug": hotel.slug})

        data = {
            "name": "updated hotel",
            "location": TEST_LOCATION[1][0],
        }

        response = self.client.patch(url, data, format="json")

        result = response.status_code
        expected = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(result, expected, msg=response.json())

    def test_delete(self):
        """
        Test delete without authentication

        Expected: 401
        """
        hotel_name = "test hotel"

        hotel = Hotel.objects.get(name=hotel_name)
        url = reverse("hotel-detail", kwargs={"slug": hotel.slug})

        response = self.client.delete(url)

        result = response.status_code
        expected = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(result, expected)
