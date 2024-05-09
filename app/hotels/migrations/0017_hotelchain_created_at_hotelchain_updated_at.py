# Generated by Django 4.0.4 on 2024-04-15 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0016_alter_hotelchain_price_range_alter_hotelchain_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotelchain",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hotelchain",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]