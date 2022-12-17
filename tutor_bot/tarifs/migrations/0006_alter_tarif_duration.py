# Generated by Django 4.1.2 on 2022-12-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarifs', '0005_alter_tarif_duration_alter_tarif_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarif',
            name='duration',
            field=models.PositiveSmallIntegerField(choices=[(0, 'бессрочно'), (1, '1 месяц'), (3, '3 месяца'), (5, '5 месяцев'), (9, '9 месяцев'), (10, '10 месяцев')], unique=True, verbose_name='Тарифы'),
        ),
    ]