from django.db import models

from bots.models import Bot
from users.models import Student


class Category(models.Model):
    """Модель категорий заданий."""

    name = models.CharField(
        verbose_name='Категория (тема)',
        max_length=100)
    is_active = models.BooleanField(
        verbose_name='Активна?',
        default=False)
    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='category')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель заданий."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=50)
    text = models.TextField(
        verbose_name='Текст задания',
        max_length=3900)
    answer = models.CharField(
        verbose_name='Ответ',
        max_length=100)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='task')
    time = models.DateTimeField(
        verbose_name='Дата выдачи',
        blank=True,
        null=True)
    img = models.ImageField(
        verbose_name='Изображение',
        upload_to='temp/',
        blank=True)
    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='task')

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


class Log(models.Model):
    """Модель выдачи заданий."""

    student = models.ForeignKey(
        Student,
        verbose_name='Учащийся',
        on_delete=models.CASCADE,
        related_name='log')
    task = models.ForeignKey(
        Task,
        verbose_name='Задание',
        on_delete=models.CASCADE,
        related_name='log')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='log')
    answer = models.CharField(
        verbose_name='Ответ',
        max_length=100)
    is_truth = models.BooleanField(
        verbose_name='Верно?',
        default=False)
    time = models.DateTimeField(
        verbose_name='Дата ответа',
        auto_now=True)
    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='log')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('-time',)
