# Generated by Django 5.0.7 on 2024-08-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="emailActivated",
            field=models.BooleanField(default=False),
        ),
    ]
