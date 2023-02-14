# Generated by Django 4.1.2 on 2023-02-14 07:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("bots", "0011_alter_bot_tarif"),
    ]

    operations = [
        migrations.AddField(
            model_name="bot",
            name="last_rating",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name="Дата последнего рейтинга",
            ),
        ),
    ]
