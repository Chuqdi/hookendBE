# Generated by Django 5.0.6 on 2024-07-07 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_religion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ethnicity',
            field=models.TextField(blank=True, null=True),
        ),
    ]
