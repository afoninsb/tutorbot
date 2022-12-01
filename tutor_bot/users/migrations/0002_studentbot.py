# Generated by Django 4.1.2 on 2022-11-12 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Активирован?')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bots.bot', verbose_name='Бот')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student', verbose_name='Учащийся')),
            ],
        ),
    ]
