# Generated by Django 4.1.7 on 2023-04-30 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("KODBURG", "0008_remove_user_connected_user_connected_from_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="connected_from",
        ),
        migrations.RemoveField(
            model_name="user",
            name="connected_to",
        ),
        migrations.CreateModel(
            name="Requests",
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
                    "user_from",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_fromReq",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_toReq",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]