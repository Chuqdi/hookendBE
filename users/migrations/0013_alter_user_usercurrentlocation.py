# Generated by Django 5.0.7 on 2024-09-16 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_user_usercurrentlocation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="userCurrentLocation",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]
