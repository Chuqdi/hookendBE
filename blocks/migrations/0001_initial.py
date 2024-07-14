# Generated by Django 5.0.6 on 2024-07-13 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_blocked', models.DateTimeField(auto_now_add=True)),
                ('blocked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_blocked', to=settings.AUTH_USER_MODEL)),
                ('blocking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_who_blocked_me', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]