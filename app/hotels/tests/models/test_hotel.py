from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from app.hotels.models import photo_directory_path
from app.hotels.models import Hotel, HotelChain
from ..base import image_path


class HotelTestCase(TestCase):
    def setUp(self):
        with open(image_path, "rb") as f:
            Hotel.objects.create(
                name="test hotel",
                location="test land",
                photo=SimpleUploadedFile("test.png", f.read(), "image/png"),
            )

    def test_as_string(self):
        test_hotel = Hotel.objects.get(name="test hotel")
        self.assertEqual(str(test_hotel), f"{test_hotel.name}, {test_hotel.location}")

    def test_full_name(self):
        test_hotel = Hotel.objects.get(name="test hotel")
        self.assertEqual(test_hotel.full_name, "test hotel, test land")

    def test_slug(self):
        test_hotel = Hotel.objects.get(name="test hotel")
        self.assertEqual(test_hotel.slug, "test-hotel")

    def test_slug_unique(self):
        with open(image_path, "rb") as f:
            Hotel.objects.create(
                name="test´hotel",  # slugify -> test-hotel
                location="test land",
                photo=SimpleUploadedFile("test.png", f.read(), "image/png"),
            )

        self.assertEqual(Hotel.objects.filter(slug="test-hotel").count(), 1)

    def test_get_absolute_url(self):
        test_hotel = Hotel.objects.get(name="test hotel")

        expected = reverse("hotel-detail", kwargs={"slug": test_hotel.slug})
        result = test_hotel.get_absolute_url()
        self.assertEqual(result, expected, msg=f"{result} != {expected}")


class HotelPhotoDirectoryPathTestCase(TestCase):
    def setUp(self):
        with open(image_path, "rb") as f:
            Hotel.objects.create(
                name="test hotel",
                location="test land",
                slug="test-hotel-test-land",
                photo=SimpleUploadedFile("test.png", f.read(), "image/png"),
            )

    def test_photo_directory_path(self):
        instance = Hotel.objects.get(name="test hotel")
        filename = "test.png"
        expected_ext = "png"
        expected_path = instance.photo.path

        result = photo_directory_path(instance, filename)

        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("hotels/"))
        self.assertTrue(result.endswith(expected_ext))
        self.assertTrue(len(result), len(expected_path))

    def test_photo_directory_path_no_extension(self):
        instance = Hotel.objects.get(name="test hotel")
        filename = "test"
        expected_ext = ""
        expected_path = instance.photo.path

        result = photo_directory_path(instance, filename)

        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("hotels/"))
        self.assertTrue(result.endswith(expected_ext))
        self.assertTrue(len(result), len(expected_path))

    def test_photo_directory_path_malformed_filename(self):
        instance = Hotel.objects.get(name="test hotel")
        filename = ".test.png"
        expected_ext = "png"
        expected_path = instance.photo.path

        result = photo_directory_path(instance, filename)

        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("hotels/"))
        self.assertTrue(result.endswith(expected_ext))
        self.assertTrue(len(result), len(expected_path))


class HotelAssignChainTestCase(TestCase):
    def setUp(self) -> None:
        self.hotel = Hotel.objects.create(name="test hotel")
        self.chain = HotelChain.objects.create(title="test chain")
        super().setUp()

    def test_assign_chain_already_set(self):
        self.hotel.chain = self.chain
        self.hotel.save()

        self.hotel.assign_chain()

        self.assertEqual(
            self.hotel.chain, self.chain, msg=f"{self.hotel.chain} != {self.chain}"
        )

    def test_assign_chain_auto_assign(self):
        HotelChain.objects.create(title="test hotel", auto_assign=True)

        self.hotel.assign_chain()

        self.assertEqual(
            self.hotel.chain.title,  # type: ignore
            "Test Hotel",
            msg=f"{self.hotel.chain.title} != Test Hotel",  # type: ignore
        )

    def test_assign_chain_no_auto_assign(self):
        HotelChain.objects.create(title="test hotel", auto_assign=False)

        self.hotel.assign_chain()

        self.assertIsNone(self.hotel.chain)

    def test_assign_chain_multiple_auto_assign(self):
        HotelChain.objects.create(title="test hotel 1", auto_assign=True)
        HotelChain.objects.create(title="test hotel 2", auto_assign=True)

        self.hotel.assign_chain()

        self.assertIn(self.hotel.chain.title, ["Test Hotel 1", "Test Hotel 2"])  # type: ignore

    def test_assign_chain_no_matching_chain(self):
        self.hotel.assign_chain()

        self.assertIsNone(self.hotel.chain, msg=f"{self.hotel.chain} != None")

    def test_assign_though_signal_post_save(self):
        chain = HotelChain.objects.create(title="test hotel", auto_assign=True)
        self.hotel.chain = chain
        self.hotel.save()

        self.assertEqual(
            self.hotel.chain.title,
            "Test Hotel".title(),
            msg=f"{self.hotel.chain.title} != Test Hotel".title(),
        )

    def test_assign_title_shorter_than_3(self):
        HotelChain.objects.create(title="te", auto_assign=True)

        self.hotel.assign_chain()

        self.assertIsNone(self.hotel.chain, msg=f"{self.hotel.chain} != None")

    def test_assign_auto_assign_false(self):
        HotelChain.objects.create(title="test hotel", auto_assign=False)

        self.hotel.assign_chain()

        self.assertIsNone(self.hotel.chain, msg=f"{self.hotel.chain} != None")


class HotelAssignRelatedHotelsTestCase(TestCase):
    def setUp(self) -> None:
        self.chain = HotelChain.objects.create(title="test chain")
        self.hotel1 = Hotel.objects.create(name="Hotel 1", chain=self.chain)
        self.hotel2 = Hotel.objects.create(name="Hotel 2", chain=self.chain)
        self.hotel3 = Hotel.objects.create(name="Hotel 3", chain=self.chain)
        self.hotel4 = Hotel.objects.create(name="Hotel 4", chain=self.chain)
        self.hotel5 = Hotel.objects.create(name="Hotel 5")

        return super().setUp()

    def test_assign_related_hotels_with_chain(self):
        self.hotel1.assign_related_hotels()

        expected = len([self.hotel2, self.hotel3, self.hotel4])
        result = self.hotel1.related_hotels.count()

        self.assertEqual(expected, result, msg=f"{expected} != {result}")

    def test_assign_related_hotels_without_chain(self):
        result = self.hotel5.related_hotels.count()
        expected = 0
        self.assertEqual(expected, result, msg=f"{expected} != {result}")

    def test_assign_related_hotels_after_update_add_chain(self):
        # Add hotel5 to the chain
        self.hotel5.chain = self.chain
        self.hotel5.save()

        expected = len([self.hotel1, self.hotel2, self.hotel3, self.hotel4])
        result = self.hotel5.related_hotels.count()

        self.assertEqual(expected, result, msg=f"{expected} != {result}")

    def test_assign_related_hotels_after_update_remove_chain(self):
        self.hotel1.chain = None
        self.hotel1.save()

        expected = 0
        result = self.hotel1.related_hotels.count()

        self.assertEqual(expected, result, msg=f"{expected} != {result}")

    def test_assign_related_hotels_after_update_change_chain(self):
        chain = HotelChain.objects.create(title="test chain 2")
        self.hotel1.chain = chain
        self.hotel1.save()

        expected = 0
        result = self.hotel1.related_hotels.count()

        self.assertEqual(expected, result, msg=f"{expected} != {result}")
