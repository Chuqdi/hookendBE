# Generated by Django 5.0.6 on 2024-07-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_kids'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='educationLevel',
            field=models.TextField(blank=True, null=True),
        ),
    ]
