# Generated by Django 5.0.7 on 2024-09-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_remove_user_defaultsfiltervalues_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="countryOfOrigin",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="stateOfOrigin",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="useradvancedfilter",
            name="countryOfOrigin",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="useradvancedfilter",
            name="stateOfOrigin",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
