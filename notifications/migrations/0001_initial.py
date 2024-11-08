# Generated by Django 5.0.7 on 2024-07-29 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("message", models.TextField()),
                ("notification_type", models.CharField(max_length=255)),
                ("date_sent", models.DateTimeField(auto_now_add=True)),
                ("likedPhoto", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "notification_sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "notified_users",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications_recieved",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
