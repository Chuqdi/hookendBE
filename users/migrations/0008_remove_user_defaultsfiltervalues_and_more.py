# Generated by Django 5.0.7 on 2024-09-10 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_userdefaultsfilter_user_defaultsfiltervalues"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="defaultsFilterValues",
        ),
        migrations.DeleteModel(
            name="UserDefaultsFilter",
        ),
    ]
