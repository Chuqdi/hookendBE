# Generated by Django 5.0.7 on 2024-08-22 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("likes", "0004_like_likedimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="like",
            name="likedImage",
        ),
    ]