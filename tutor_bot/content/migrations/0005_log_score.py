# Generated by Django 4.1.2 on 2022-12-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_log_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='score',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Балл'),
            preserve_default=False,
        ),
    ]
