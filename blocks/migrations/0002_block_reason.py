# Generated by Django 5.0.6 on 2024-07-13 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='reason',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
