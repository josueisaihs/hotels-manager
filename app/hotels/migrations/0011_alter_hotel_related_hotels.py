# Generated by Django 4.0.4 on 2024-04-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0010_alter_hotelchain_options_hotel_chain_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="related_hotels",
            field=models.ManyToManyField(blank=True, to="hotels.hotel"),
        ),
    ]