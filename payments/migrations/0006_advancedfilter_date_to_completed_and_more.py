# Generated by Django 5.0.7 on 2024-07-29 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_boostedprofile_delete_parentsub"),
    ]

    operations = [
        migrations.AddField(
            model_name="advancedfilter",
            name="date_to_completed",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="boostedprofile",
            name="date_to_completed",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="premium",
            name="date_to_completed",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="premiumhooked",
            name="date_to_completed",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="wildfeature",
            name="date_to_completed",
            field=models.DateField(blank=True, null=True),
        ),
    ]
