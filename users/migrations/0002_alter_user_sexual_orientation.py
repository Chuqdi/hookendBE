# Generated by Django 5.0.6 on 2024-07-07 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sexual_orientation',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
