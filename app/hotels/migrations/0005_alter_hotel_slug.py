# Generated by Django 4.0.4 on 2022-04-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0004_hotel_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]
