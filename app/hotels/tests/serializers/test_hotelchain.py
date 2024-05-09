from datetime import datetime, timezone

from django.test import RequestFactory, TestCase

from app.hotels.models import HotelChain
from app.hotels.serializers import HotelChainSerializer
from ..base import ignore_fields, simple_msg


class HotelChainSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.chain = HotelChain(title="test title", price_range=2)
        self.chain.save()

        self.ignore_fields = [
            "updated_at",
            "created_at",
            "recipient_email",
            "auto_assign",
        ]

    def test_create_with_hyperlink_field(self):
        """
        Test if the URL is generated correctly
        Use context -> request to generate the URL
        """
        expected_data = {
            "url": "http://testserver/api/v1/hotelchains/test-title/",
            "price_range": 2,
            "title": "test title",
            "slug": "test-title",
            "description": "",
            "email": "",
            "phone": "",
            "website": "",
            "recipient_email": "",
            "auto_assign": False,
            "sales_contact": "",
            "price_tag": HotelChain.PRICE_TAGS[2],
            "number_of_hotels": 0,
            "updated_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
            "created_at": str(
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            ),  # Ignore in test case
        }

        request = self.factory.get("/api/v1/hotelchains/")
        results = HotelChainSerializer(self.chain, context={"request": request}).data
        results = dict(results)

        # Test if the date is in the expected format
        self.assertEqual(len(results["created_at"]), len(expected_data["created_at"]))
        self.assertEqual(len(results["updated_at"]), len(expected_data["updated_at"]))

        results = ignore_fields(results, self.ignore_fields)
        expected_data = ignore_fields(expected_data, self.ignore_fields)
        expected_data["title"] = expected_data["title"].title()
        self.assertDictEqual(results, expected_data, simple_msg(expected_data, results))

    def test_create(self):
        expected_data = {
            "price_range": 2,
            "title": "test title",
            "slug": "test-title",
            "description": "",
            "email": "",
            "phone": "",
            "website": "",
            "recipient_email": "",
            "auto_assign": False,
            "sales_contact": "",
            "price_tag": HotelChain.PRICE_TAGS[2],
            "number_of_hotels": 0,
        }

        serializer = HotelChainSerializer(data=expected_data)
        is_valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(is_valid, serializer.errors)

        chain = serializer.save()
        self.assertIsInstance(
            chain, HotelChain, msg=simple_msg(type(HotelChain), type(chain))
        )

        result = chain.title  # type: ignore
        expected = expected_data["title"].title()
        self.assertEqual(result, expected, msg=simple_msg(expected, result))  # type: ignore

        result = chain.price_range  # type: ignore
        expected = expected_data["price_range"]
        self.assertEqual(result, expected, simple_msg(expected, result))

    def test_invalid_data(self):
        expected_data = {
            "price_range": 2,
            "title": "test title",
            "slug": "test-title",
            "description": "",
            "email": "",
            "phone": "",
            "website": "",
            "recipient_email": "",
            "auto_assign": False,
            "sales_contact": "",
            "price_tag": HotelChain.PRICE_TAGS[2],
            "number_of_hotels": 0,
        }

        data = expected_data.copy()
        data["price_range"] = 0  # Invalid price range 1 < price_range < 4

        serializer = HotelChainSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid, serializer.errors)

    def test_update(self):
        expected_data = {
            "price_range": self.chain.price_range,
            "title": "test title",
            "slug": "test-title",
            "description": "Update description",
            "email": "",
            "phone": "",
            "website": "",
            "recipient_email": "",
            "auto_assign": False,
            "sales_contact": "",
            "price_tag": self.chain.price_tag,
            "number_of_hotels": 0,
        }

        expected_data["price_range"] = 3

        serializer = HotelChainSerializer(self.chain, data=expected_data, partial=True)
        is_valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(is_valid, serializer.errors)

        chain = serializer.save()

        result = chain.price_range  # type: ignore
        expected = expected_data["price_range"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

        result = chain.description  # type: ignore
        expected = expected_data["description"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

    def test_serializer_method_field(self):
        expected_data = {
            "price_range": 2,
            "title": "test title",
            "slug": "test-title",
            "description": "",
            "email": "",
            "phone": "",
            "website": "",
            "sales_contact": "",
            "recipient_email": "",
            "auto_assign": False,
            "price_tag": HotelChain.PRICE_TAGS[2],
            "number_of_hotels": 0,
        }

        serializer = HotelChainSerializer(data=expected_data)
        self.assertTrue(serializer.is_valid(raise_exception=True), serializer.errors)
        chain = serializer.save()

        result = chain.price_tag  # type: ignore
        expected = HotelChain.PRICE_TAGS[2]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

        result = chain.number_of_hotels  # type: ignore
        expected = 0
        self.assertEqual(result, expected, msg=simple_msg(expected, result))
