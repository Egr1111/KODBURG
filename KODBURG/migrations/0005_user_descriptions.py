# Generated by Django 4.1.7 on 2023-04-02 15:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("KODBURG", "0004_user_notice"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="descriptions",
            field=models.ManyToManyField(
                blank=True, related_name="Descriptions", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
