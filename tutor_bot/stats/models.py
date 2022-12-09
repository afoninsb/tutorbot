from django.db import models

from bots.models import Bot
from users.models import Student


class Rating(models.Model):
    """Модель рейтинга."""

    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='rating')
    student = models.ForeignKey(
        Student,
        verbose_name='Учащийся',
        on_delete=models.CASCADE,
        related_name='rating')
    time = models.DateField(
        verbose_name='Дата',
        auto_now=True,)
    score = models.PositiveSmallIntegerField(
        verbose_name='Балл',
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('-score',)
