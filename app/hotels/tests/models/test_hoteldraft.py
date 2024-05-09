from django.test import TestCase

from app.hotels.models import Hotel, HotelChain, HotelDraft
from ..base import User


class HotelDraftTestCase(TestCase):
    def setUp(self) -> None:
        self.hotel = Hotel.objects.create(name="test hotel")
        self.chain = HotelChain.objects.create(title="test chain")
        self.user = User.objects.create_user(email="test@test.com", password="foo")  # type: ignore
        return super().setUp()

    def test_create(self):
        HotelDraft.objects.create(
            hotel=self.hotel,
            chain=self.chain,
            created_by=self.user,
            name="new hotel name",
            location="new hotel location",
        )

        self.assertEqual(HotelDraft.objects.count(), 1)

    def test_approve_and_save(self):
        draft = HotelDraft.objects.create(
            hotel=self.hotel,
            chain=self.chain,
            created_by=self.user,
            name="new hotel name",
            location="new hotel location",
        )

        self.assertNotEqual(draft.name, draft.hotel.name)

        draft.approved_and_save()

        self.assertEqual(draft.name, draft.hotel.name)
