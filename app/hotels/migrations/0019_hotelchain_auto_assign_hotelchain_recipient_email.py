# Generated by Django 4.0.4 on 2024-04-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hotels", "0018_alter_hotelchain_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotelchain",
            name="auto_assign",
            field=models.BooleanField(
                default=False,
                help_text="If the chain should be auto assigned based on the title",
                verbose_name="Auto Assign",
            ),
        ),
        migrations.AddField(
            model_name="hotelchain",
            name="recipient_email",
            field=models.EmailField(
                blank=True,
                help_text="Email to receive notifications when a hotel is created",
                max_length=50,
                verbose_name="Recipient Email",
            ),
        ),
    ]
