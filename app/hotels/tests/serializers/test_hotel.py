from datetime import datetime, timezone

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from django.urls import reverse

from app.hotels.models import Hotel, HotelChain, photo_directory_path
from app.hotels.serializers import HotelSerializer
from ..base import image_path, TEST_LOCATION, ignore_fields, simple_msg


class HotelSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.ignore_fields = ["photo", "created_at", "updated_at"]

        self.filename = "test.png"
        with open(image_path, "rb") as f:
            self.hotel = Hotel.objects.create(
                name="test hotel",
                photo=SimpleUploadedFile(self.filename, f.read(), "image/png"),
            )

    def test_create_with_hyperlink_field(self):
        """
        Test if the URL is generated correctly
        Use context -> request to generate the URL
        """
        expected_data = {
            "url": "http://testserver/api/v1/hotels/test-hotel/",
            "chain": None,
            "related_hotels": [],
            "updated_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
            "created_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
            "name": "test hotel",
            "photo": "http://testserver/media/hotels/deccd130-74a1-457b-9e16-b72afd3cd64c.png",  # Ignore in test case
            "slug": "test-hotel",
            "is_active": False,
            "location": TEST_LOCATION[0][0],
        }

        request = self.factory.get("/api/v1/hotels/")
        results = HotelSerializer(self.hotel, context={"request": request}).data
        results = dict(results)

        # Convert the related hotels to list of dict
        results["related_hotels"] = [dict(hotel) for hotel in results["related_hotels"]]

        # Test URL
        result = (
            reverse("hotel-detail", kwargs={"slug": self.hotel.slug}) in results["url"]
        )
        self.assertTrue(
            result,
            msg=f"Expected {reverse('hotel-detail', kwargs={'slug': self.hotel.slug})} in {results['url']}",
        )

        # Test if the date is in the expected format
        self.assertEqual(len(results["created_at"]), len(expected_data["created_at"]))
        self.assertEqual(len(results["updated_at"]), len(expected_data["updated_at"]))

        # Photo URL Generation
        expected_data_photo_url = (
            f"http://testserver/media/{photo_directory_path(self.hotel, self.filename)}"
        )
        self.assertEqual(len(results["photo"]), len(expected_data_photo_url))

        # Remove the fields that are not relevant for the test
        # this fields are not relevant because they are dynamic
        results = ignore_fields(results, self.ignore_fields)
        expected_data = ignore_fields(expected_data, self.ignore_fields)
        expected_data["id"] = self.hotel.pk

        self.assertDictEqual(results, expected_data)

    def test_create_with_nested_serialization(self):
        chain = HotelChain.objects.create(title="test chain", price_range=2)

        expected_data = {
            "url": "http://testserver/api/v1/hotels/test-hotel/",
            "chain": {"id": chain.pk, "title": "test chain"},
            "related_hotels": [],
            "updated_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
            "created_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
            "name": "test hotel 2",
            "photo": "http://testserver/media/hotels/deccd130-74a1-457b-9e16-b72afd3cd64c.png",  # Ignore in test case
            "slug": "test-hotel",
            "is_active": False,
            "location": None,
        }

        request = self.factory.get("/api/v1/hotels/")
        hotel = Hotel.objects.create(name=expected_data["name"], chain=chain)
        results = dict(HotelSerializer(hotel, context={"request": request}).data)

        results = dict(results["chain"])

        result = chain.title  # type: ignore
        expected = expected_data["chain"]["title"].title()
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

    def test_create(self):
        expected_data = {
            "name": "new test hotel",
            "chain": {"title": "test chain", "price_range": 3},
        }

        data = expected_data.copy()

        serializer = HotelSerializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(is_valid, serializer.errors)

        hotel = serializer.save()
        self.assertIsInstance(hotel, Hotel, msg=simple_msg(type(Hotel), type(hotel)))

        result = hotel.name  # type: ignore
        expected = expected_data["name"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

        result = hotel.chain.title  # type: ignore
        expected = expected_data["chain"]["title"].title()
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

        result = hotel.chain.price_range  # type: ignore
        expected = expected_data["chain"]["price_range"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))  # type: ignore

    def test_required_name_field(self):
        expected_data = {"chain": {"title": "test chain", "price_range": 3}}

        data = expected_data.copy()

        serializer = HotelSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid, serializer.errors)

    def test_invalid_nested_data(self):
        expected_data = {
            "name": "test hotel 2",
            "chain": {"title": "test chain", "price_range": 0},
        }

        data = expected_data.copy()

        serializer = HotelSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid, serializer.errors)

    def test_update(self):
        expected_data = {
            "name": self.hotel.name,
            "chain": {"title": "test chain", "price_range": 3},
        }

        data = {
            "name": "updated test hotel",
            "chain": {"title": "test chain", "price_range": 3},
        }

        serializer = HotelSerializer(self.hotel, data=data, partial=True)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)

        hotel = serializer.save()

        result = hotel.name  # type: ignore
        expected = expected_data["name"]
        self.assertNotEqual(result, expected, msg=simple_msg(expected, result))

        result = hotel.name  # type: ignore
        expected = data["name"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

    def test_update_partial_creating_chain(self):
        """
        Test if the chain is created if it does not exist
        """

        data = {
            "name": "updated test hotel",
            "chain": {"title": "test chain", "price_range": 4},
        }

        old_chain_type = self.hotel.chain
        self.assertIsNone(old_chain_type, msg=simple_msg(None, old_chain_type))

        serializer = HotelSerializer(self.hotel, data=data, partial=True)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)

        hotel = serializer.save()

        self.assertNotEqual(type(old_chain_type), type(hotel.chain), msg=simple_msg(type(old_chain_type), type(hotel.chain)))  # type: ignore
        self.assertIsInstance(hotel.chain, HotelChain, msg=simple_msg(type(HotelChain), type(hotel.chain)))  # type: ignore

        chain_query = HotelChain.objects.filter(title__iexact="test chain")
        self.assertTrue(chain_query.exists(), msg="Chain not found")
        self.assertEqual(chain_query.count(), 1, msg="Multiple chains found")

        chain = chain_query.first()
        result = chain.price_range  # type: ignore
        expected = data["chain"]["price_range"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

    def test_update_partial_updating_chain_name(self):
        """
        Test if the chain is updated if it exists
        """
        hotel = Hotel.objects.create(
            name="new test hotel",
            chain=HotelChain.objects.create(title="test chain", price_range=3),
        )

        data = {"chain": {"title": "updated test chain", "price_range": 4}}

        serializer = HotelSerializer(hotel, data=data, partial=True)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)

        hotel = serializer.save()

        old_chain_query = HotelChain.objects.filter(title__iexact="test chain")
        self.assertFalse(old_chain_query.exists(), msg="Chain found")

        chain_query = HotelChain.objects.filter(title__iexact=data["chain"]["title"])
        self.assertTrue(chain_query.exists(), msg="Chain not found")
        self.assertEqual(chain_query.count(), 1, msg="Multiple chains found")

        chain = chain_query.first()
        result = chain.price_range  # type: ignore
        expected = data["chain"]["price_range"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))
