# Generated by Django 4.1.2 on 2022-12-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_log_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='time',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата ответа'),
        ),
    ]
