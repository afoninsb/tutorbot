# Generated by Django 4.1.2 on 2023-02-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0003_alter_rating_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="time",
            field=models.CharField(max_length=10, verbose_name="Дата"),
        ),
    ]
