# Generated by Django 5.0.7 on 2024-08-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_alter_advancedfilter_productid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advancedfilter",
            name="productId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="boostedprofile",
            name="productId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="premiumhooked",
            name="productId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="premiumplus",
            name="productId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="wildfeature",
            name="productId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
