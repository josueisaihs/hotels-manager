# Generated by Django 4.0.4 on 2024-04-13 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0012_alter_hotelchain_slug"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="hotel",
            options={"verbose_name": "Hotel", "verbose_name_plural": "Hotels"},
        ),
        migrations.AlterModelOptions(
            name="hotelchain",
            options={
                "verbose_name": "Hotel Chain",
                "verbose_name_plural": "Hotel Chains",
            },
        ),
    ]