# Generated by Django 5.0.7 on 2024-09-10 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_useremailactivationcode_date_created"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDefaultsFilter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sexual_orientation",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "what_you_are_looking_for",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "relationship_status",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("interests", models.TextField(blank=True, null=True)),
                ("bio", models.TextField(blank=True, null=True)),
                ("school", models.TextField(blank=True, null=True)),
                ("company_name", models.TextField(blank=True, null=True)),
                ("readyForFamily", models.TextField(blank=True, null=True)),
                ("work_title", models.TextField(blank=True, null=True)),
                ("language", models.TextField(blank=True, null=True)),
                ("drink", models.TextField(blank=True, null=True)),
                ("drug", models.TextField(blank=True, null=True)),
                ("kids", models.TextField(blank=True, null=True)),
                ("introvert", models.TextField(blank=True, null=True)),
                ("educationLevel", models.TextField(blank=True, null=True)),
                ("relationshipGoal", models.TextField(blank=True, null=True)),
                ("starSign", models.TextField(blank=True, null=True)),
                ("pets", models.TextField(blank=True, null=True)),
                ("gender", models.TextField(blank=True, null=True)),
                ("religion", models.TextField(blank=True, null=True)),
                ("ethnicity", models.TextField(blank=True, null=True)),
                ("country", models.TextField(blank=True, max_length=200, null=True)),
                ("state", models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="defaultsFilterValues",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.userdefaultsfilter",
            ),
        ),
    ]