from django.test import TestCase
from django.urls import reverse

from app.hotels.models import HotelChain


class HotelChainTestCase(TestCase):
    def test_as_string(self):
        test_hotel_chain = HotelChain.objects.create(title="test hotel chain")
        self.assertEqual(str(test_hotel_chain), test_hotel_chain.title)

    def test_verbose_name(self):
        self.assertEqual(HotelChain._meta.verbose_name, "Hotel Chain")

    def test_verbose_name_plural(self):
        self.assertEqual(HotelChain._meta.verbose_name_plural, "Hotel Chains")

    def test_get_absolute_url(self):
        test_hotel_chain = HotelChain.objects.create(title="test hotel chain")

        result = test_hotel_chain.get_absolute_url()
        expected = reverse("hotelchain-detail", kwargs={"slug": test_hotel_chain.slug})
        self.assertEqual(result, expected, msg=f"{result} != {expected}")

    def test_price_tag(self):
        test_hotel_chain = HotelChain.objects.create(
            title="test hotel chain", price_range=1
        )

        result = test_hotel_chain.price_tag
        expected = test_hotel_chain.PRICE_TAGS[1]
        self.assertEqual(result, expected, msg=f"{result} != {expected}")

    def test_number_of_hotels(self):
        test_hotel_chain = HotelChain.objects.create(title="test hotel chain")

        result = test_hotel_chain.number_of_hotels
        expected = test_hotel_chain.hotel_set.count()  # type: ignore
        self.assertEqual(result, expected, msg=f"{result} != {expected}")

    def test_slug(self):
        test_hotel_chain = HotelChain.objects.create(title="test hotel chain")

        result = test_hotel_chain.slug
        expected = "test-hotel-chain"
        self.assertEqual(result, expected, msg=f"{result} != {expected}")

    def test_slug_unique(self):
        HotelChain.objects.create(title="test´hotel chain")

        self.assertEqual(HotelChain.objects.filter(slug="test-hotel-chain").count(), 1)

    def test_title_unique(self):
        HotelChain.objects.create(title="test hotel chain 2")
        HotelChain.objects.create(title="test hotel chain 2".title())
        HotelChain.objects.create(title="test hotel chain 2".capitalize())

        HotelChain.objects.create(title="test hotel chain 3")
        HotelChain.objects.create(title="test hotel chain 3".lower())
        HotelChain.objects.create(title="test hotel chain 3".upper())
        HotelChain.objects.create(title="test hotel chain 3".title())

        self.assertEqual(
            HotelChain.objects.filter(title="test hotel chain 2".title()).count(), 1
        )
        self.assertEqual(
            HotelChain.objects.filter(title="test hotel chain 3".title()).count(), 1
        )
