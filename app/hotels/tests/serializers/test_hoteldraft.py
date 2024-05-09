from django.test import RequestFactory, TestCase
from django.urls import reverse

from app.hotels.models import Hotel, HotelChain, HotelDraft
from app.hotels.serializers import HotelDraftSerializer
from ..base import TEST_LOCATION, simple_msg, User


class HotelDraftSerializerTestCase(TestCase):
    def setUp(self) -> None:

        self.chain = HotelChain.objects.create(
            title="test chain updated", price_range=2
        )
        chain_init = HotelChain.objects.create(title="test chain", price_range=2)

        self.hotel = Hotel.objects.create(name="test hotel", chain=chain_init)
        self.user = User.objects.create_user(email="test@test.com", password="foo")  # type: ignore

        self.factory = RequestFactory()
        self.request = self.factory.get("/api/v1/hoteldrafts/")
        self.request.user = self.user

        self.data_sample = {
            "hotel": self.hotel.slug,
            "name": "test hotel updated",
            "location": TEST_LOCATION[0][0],
            "chain": {"title": "test chain updated", "price_range": 2},
        }

        self.ignore_fields = ["photo", "created_at", "updated_at"]

    def test_create_with_hyperlink_field(self):
        """
        Test if the URL is generated correctly
        Use context -> request to generate the URL
        """

        hoteldraft = HotelDraft.objects.create(
            hotel=self.hotel,
            name="test hotel updated",
            location=TEST_LOCATION[1][0],
            chain=self.chain,
            created_by=self.user,
        )

        results = HotelDraftSerializer(
            instance=hoteldraft, context={"request": self.request}
        ).data
        results = dict(results)

        # Test URL
        result = (
            reverse("hoteldraft-detail", kwargs={"slug": hoteldraft.slug})
            in results["url"]
        )
        self.assertTrue(
            result,
            msg=f"Expected {reverse('hoteldraft-detail', kwargs={'slug': hoteldraft.slug})} in {results['url']}",
        )

    def test_as_data(self):
        serializer = HotelDraftSerializer(
            data=self.data_sample, context={"request": self.request}
        )
        is_valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(is_valid, serializer.errors)

        hoteldraft = serializer.save(created_by=self.user)
        self.assertIsInstance(
            hoteldraft, HotelDraft, msg=simple_msg(type(HotelDraft), type(hoteldraft))
        )

        result = hoteldraft.name  # type: ignore
        expected = self.data_sample["name"]
        self.assertEqual(result, expected, msg=simple_msg(expected, result))

        result = hoteldraft.chain.title  # type: ignore
        expected = self.data_sample["chain"]["title"].title()
        self.assertEqual(result, expected, msg=simple_msg(expected, result))
