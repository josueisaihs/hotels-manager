# Generated by Django 4.0.4 on 2024-04-19 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0021_hoteldraft_delete_hotelupdate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hoteldraft",
            name="related_hotels",
        ),
    ]
