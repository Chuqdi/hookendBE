# Generated by Django 5.0.6 on 2024-07-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_user_profile_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.TextField(blank=True, null=True),
        ),
    ]
