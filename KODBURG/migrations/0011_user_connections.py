# Generated by Django 4.1.7 on 2023-04-30 22:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("KODBURG", "0010_requests_onl_from_requests_onl_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="connections",
            field=models.ManyToManyField(
                blank=True, related_name="connections", to="KODBURG.requests"
            ),
        ),
    ]