# Generated by Django 4.0.4 on 2024-04-13 12:39

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0011_alter_hotel_related_hotels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotelchain",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False, populate_from="title", unique=True
            ),
        ),
    ]
