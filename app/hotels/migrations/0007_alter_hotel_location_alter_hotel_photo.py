# Generated by Django 4.0.4 on 2022-04-24 13:24

from django.db import migrations, models
import app.hotels.models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0006_alter_hotel_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="location",
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="hotel",
            name="photo",
            field=models.ImageField(upload_to=app.hotels.models.photo_directory_path),
        ),
    ]
