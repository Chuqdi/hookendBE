# Generated by Django 5.0.7 on 2024-07-20 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_advancedfiltervalues'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.TextField(blank=True, null=True),
        ),
    ]
