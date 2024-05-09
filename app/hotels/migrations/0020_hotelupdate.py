# Generated by Django 4.0.4 on 2024-04-19 05:22

import app.config.utils
import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hotels", "0019_hotelchain_auto_assign_hotelchain_recipient_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="HotelUpdate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "location",
                    models.CharField(
                        db_index=True, max_length=50, null=True, verbose_name="Location"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        upload_to=app.config.utils.photo_directory_path,
                        verbose_name="Photo",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="Is Active"
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, max_length=50, verbose_name="Name"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        max_length=250,
                        populate_from="name",
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        db_index=True,
                        default="pending",
                        help_text="The status of the hotel change request",
                        max_length=10,
                        verbose_name="Status",
                    ),
                ),
                (
                    "chain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hotels.hotelchain",
                        verbose_name="Chain",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user who created the update request",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        help_text="The hotel to be updated",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="hotels.hotel",
                        verbose_name="Hotel",
                    ),
                ),
                (
                    "related_hotels",
                    models.ManyToManyField(
                        blank=True,
                        to="hotels.hotelupdate",
                        verbose_name="Related Hotels",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hotel Change Request",
                "verbose_name_plural": "Hotel Change Requests",
                "ordering": ["-created_at"],
            },
        ),
    ]