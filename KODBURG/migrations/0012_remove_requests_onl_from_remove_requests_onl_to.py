# Generated by Django 4.1.7 on 2023-05-06 22:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("KODBURG", "0011_user_connections"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="requests",
            name="onl_from",
        ),
        migrations.RemoveField(
            model_name="requests",
            name="onl_to",
        ),
    ]
