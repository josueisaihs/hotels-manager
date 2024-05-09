from typing import Union

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField

from app.config.utils import photo_directory_path
from .tasks import send_notification_email
from .managers import AbstractHotelManager, HotelChainManager


User = get_user_model()


class TimestampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class HotelChain(TimestampedModel):
    """
    Hotel Chain entity

    represents a title, description, email, phone, website, sales contact and price range

    title: name of the hotel chain
    description: description of the hotel chain
    email: email of the hotel chain
    phone: phone number of the hotel chain
    website: website of the hotel chain
    sales_contact: sales contact of the hotel chain
    price_range: price range of the hotel chain
    """

    PRICE_TAGS = {1: "cheap", 2: "cheap", 3: "expensive", 4: "expensive"}

    PRICE_LOW = 1
    PRICE_MEDIUM = 2
    PRICE_HIGH = 3
    PRICE_LUXURY = 4

    PRICE_CHOICES = [
        (PRICE_LOW, "$"),
        (PRICE_MEDIUM, "$$"),
        (PRICE_HIGH, "$$$"),
        (PRICE_LUXURY, "$$$$"),
    ]

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=50,
        db_index=True,
    )
    slug = AutoSlugField(
        verbose_name=_("Slug"),
        populate_from="title",
        unique=True,
        max_length=50,
        db_index=True,
    )  # type: ignore
    description = models.TextField(verbose_name=_("Description"), blank=True)
    email = models.EmailField(verbose_name=_("Email"), max_length=50, blank=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=50, blank=True)
    website = models.URLField(verbose_name=_("Website"), max_length=250, blank=True)
    sales_contact = models.CharField(
        verbose_name=_("Sales Contact"), max_length=250, blank=True
    )
    price_range = models.PositiveSmallIntegerField(
        verbose_name=_("Price Range"),
        default=PRICE_MEDIUM,
        choices=PRICE_CHOICES,
    )

    auto_assign = models.BooleanField(
        verbose_name=_("Auto Assign"),
        default=False,
        help_text=_("If the chain should be auto assigned based on the title"),
    )
    recipient_email = models.EmailField(
        verbose_name=_("Recipient Email"),
        max_length=50,
        blank=True,
        help_text=_("Email to receive notifications when a hotel is created"),
    )

    objects = HotelChainManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Hotel Chain"
        verbose_name_plural = "Hotel Chains"

    @property
    def price_tag(self) -> str:
        """
        Returns the price tag based on the price range

        :return: price tag
        """

        return self.PRICE_TAGS[self.price_range]

    @property
    def number_of_hotels(self) -> int:
        """
        Returns the number of hotels in the chain

        :return: number of hotels
        """

        return self.hotel_set.count()  # type: ignore

    def get_absolute_url(self) -> str:
        return reverse("hotelchain-detail", kwargs={"slug": self.slug})


class AbstractHotel(TimestampedModel):
    """
    Abstract Hotel entity

    represents a location, photo, slug, is_active, chain and related hotels
    """

    location = models.CharField(
        verbose_name=_("Location"),
        max_length=50,
        blank=False,
        null=True,
        db_index=True,
        choices=settings.HOTEL_LOCATIONS,
        default=settings.HOTEL_LOCATIONS[0][0],
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        unique=False,
        blank=True,
        upload_to=photo_directory_path,
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"), default=False, db_index=True
    )
    chain = models.ForeignKey(
        HotelChain,
        verbose_name=_("Chain"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    objects = AbstractHotelManager()

    class Meta:
        abstract = True


class Hotel(AbstractHotel):
    slug = AutoSlugField(  # type: ignore
        verbose_name=_("Slug"),
        populate_from="name",
        unique=True,
        max_length=50,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        unique=True,
        max_length=50,
        blank=False,
        null=False,
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"), default=False, db_index=True
    )
    chain = models.ForeignKey(
        HotelChain,
        verbose_name=_("Chain"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    related_hotels = models.ManyToManyField(
        "self", verbose_name=_("Related Hotels"), blank=True
    )

    def __str__(self):
        return f"{self.name}, {self.location}"

    @property
    def full_name(self):
        if self.chain:
            return f"{self.name} - ({self.chain}), {self.location}"
        else:
            return str(self)

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

    def get_absolute_url(self) -> str:
        return reverse("hotel-detail", kwargs={"slug": self.slug})

    def assign_chain(self) -> None:
        """
        Assigns the chain based on the name and auto assign flag of the chain

        If the chain is already set, return
        """

        # if the chain is already set, return
        if self.chain:
            return

        chain = HotelChain.objects.filter_by_title_with_auto_assign(self.name)  # type: ignore
        if chain:
            self.chain = chain.first()

    def creation_email_notification(self) -> None:
        """
        Sends an email to the recipient with the hotel information (url)

        recipient: recipient email
        """

        if not self.chain:
            return
        if not self.chain.email:
            return

        hotel_url = self.get_absolute_url()

        subject = "New hotel created"
        message = f"This hotel has been created: <a href='{hotel_url}'>{self}</a>"
        recipients = [self.chain.email]  # type: ignore
        send_notification_email.delay(subject, message, recipients)

    def assign_related_hotels(self) -> None:
        """
        Assigns the related hotels based on the chain
        If the chain is not set, clears the related hotels
        """
        if self.chain:
            related_hotels = Hotel.objects.filter(chain=self.chain).exclude(pk=self.pk)  # type: ignore
            self.related_hotels.set(related_hotels)
        else:
            self.related_hotels.clear()


class HotelDraft(AbstractHotel):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending")),
        (STATUS_APPROVED, _("Approved")),
        (STATUS_REJECTED, _("Rejected")),
    ]

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        blank=False,
        null=False,
        db_index=True,
    )
    slug = AutoSlugField(  # type: ignore
        verbose_name=_("Slug"),
        populate_from="name",
        unique=True,
        max_length=250,
        db_index=True,
    )
    hotel = models.ForeignKey(
        Hotel,
        verbose_name=_("Hotel"),
        on_delete=models.CASCADE,
        related_name="+",
        help_text=_("The hotel to be updated"),
        blank=False,
        null=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created By"),
        on_delete=models.PROTECT,
        related_name="+",
        help_text=_("The user who created the update request"),
        blank=False,
        null=False,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
        help_text=_("The status of the hotel update request"),
    )

    class Meta:
        verbose_name = _("Hotel Draft")
        verbose_name_plural = _("Hotel Drafts")
        ordering = ["-created_at"]

    def __str__(self):
        return f"({self.status}) {self.hotel} - by {self.created_by}"

    def approved_and_save(self) -> bool:
        """
        Approves the hotel draft
        """

        if self.status == self.STATUS_APPROVED:
            return False

        if self.name and self.name != self.hotel.name:
            self.hotel.name = self.name

        if self.location and self.location != self.hotel.location:
            self.hotel.location = self.location

        if self.photo and self.photo != self.hotel.photo:
            self.hotel.photo = self.photo  # type: ignore

        if self.chain and self.chain != self.hotel.chain:
            self.hotel.chain = self.chain

        if self.is_active != self.hotel.is_active:
            self.hotel.is_active = self.is_active

        self.hotel.save()

        self.status = self.STATUS_APPROVED
        self.save()

        return True

    def get_absolute_url(self):
        return reverse("hoteldraft-detail", kwargs={"slug": self.slug})

    def creation_email_notification(self) -> None:
        """
        Sends an email to the recipient with the hotel information (url)

        recipient: recipient email
        """

        if not self.hotel.chain:
            return
        if not self.hotel.chain.email:
            return

        draft_url = self.hotel.get_absolute_url()

        subject = "New hotel created"
        message = f"This hotel has been created as draft by { self.created_by }: <a href='{ draft_url }'>{ self.hotel.name }</a>"
        recipients = list(
            User.objects.filter(is_reviewer=True).values_list("email", flat=True)
        )
        send_notification_email.delay(subject, message, recipients)
