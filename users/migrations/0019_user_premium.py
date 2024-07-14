# Generated by Django 5.0.6 on 2024-07-09 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('users', '0018_user_primary_profile_image_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='premium',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='premium', to='payments.premium'),
        ),
    ]