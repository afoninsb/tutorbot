# Generated by Django 4.1.2 on 2022-12-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(1, 'Новый ученик.'), (2, 'В категории мало задач.'), (3, 'В категории кончились задачи. Она отключена.'), (4, 'В боте кончились задачи. Он отключен.')], verbose_name='Типы алертов')),
                ('time', models.DateTimeField(verbose_name='Дата алерта')),
                ('attribute', models.PositiveIntegerField(verbose_name='ID объекта алерта')),
            ],
        ),
    ]
