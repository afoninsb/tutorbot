# Generated by Django 4.1.2 on 2022-12-11 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_alter_log_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='difficulty',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Обычный - 1'), (2, 'Трудный - 2'), (3, 'Для гениев - 3')], default=1, verbose_name='Трудность задания'),
        ),
    ]
