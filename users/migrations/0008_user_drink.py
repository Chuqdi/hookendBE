# Generated by Django 5.0.6 on 2024-07-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_company_name_user_work_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='drink',
            field=models.TextField(blank=True, null=True),
        ),
    ]
