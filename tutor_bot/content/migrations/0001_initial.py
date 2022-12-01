# Generated by Django 4.1.2 on 2022-11-12 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('bots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория (тема)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна?')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='bots.bot', verbose_name='Бот')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('text', models.TextField(max_length=3900, verbose_name='Текст задания')),
                ('answer', models.CharField(max_length=100, verbose_name='Ответ')),
                ('time', models.DateTimeField(blank=True, null=True, verbose_name='Дата выдачи')),
                ('img', models.ImageField(blank=True, upload_to='temp/', verbose_name='Изображение')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='bots.bot', verbose_name='Бот')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='content.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100, verbose_name='Ответ')),
                ('is_truth', models.BooleanField(default=False, verbose_name='Верно?')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Дата ответа')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='bots.bot', verbose_name='Бот')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='content.category', verbose_name='Категория')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='users.student', verbose_name='Учащийся')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='content.task', verbose_name='Задание')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'ordering': ('-time',),
            },
        ),
    ]
