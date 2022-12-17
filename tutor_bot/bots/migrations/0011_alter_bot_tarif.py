# Generated by Django 4.1.2 on 2022-12-17 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tarifs', '0005_alter_tarif_duration_alter_tarif_price'),
        ('bots', '0010_alter_bot_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='tarif',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='bot', to='tarifs.tarif', verbose_name='Тариф'),
        ),
    ]
