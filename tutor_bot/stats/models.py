from django.db import models

from bots.models import Bot
from users.models import Student


class Rating(models.Model):
    """Модель рейтинга."""
    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    student = models.ForeignKey(
        Student,
        verbose_name='Учащийся',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    time = models.DateField(
        verbose_name='Дата',
        )
    score = models.PositiveSmallIntegerField(
        verbose_name='Балл',
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('-score',)


class Alert(models.Model):
    """Модель алертов."""
    class AlertsTypes(models.IntegerChoices):
        """Типы алертов."""
        NEWUSER = 1, 'Новый ученик.'
        FEWTASKS = 2, 'В категории мало задач.'
        TASKSAREOVER = 3, 'В категории кончились задачи. Она отключена.'
        DISABLEBOT = 4, 'В боте кончились задачи. Он отключен.'

    difficulty = models.PositiveSmallIntegerField(
        verbose_name='Типы алертов',
        choices=AlertsTypes.choices,
    )
    time = models.DateTimeField(
        verbose_name='Дата алерта',
    )
    attribute = models.PositiveIntegerField(
        verbose_name='ID объекта алерта',
    )


class ReRating(models.Model):
    """Модель рейтинга."""
    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
        related_name='rerating'
    )
    student = models.ForeignKey(
        Student,
        verbose_name='Учащийся',
        on_delete=models.CASCADE,
        related_name='rerating'
    )
    time = models.DateField(
        verbose_name='Дата',
        )
    score = models.PositiveSmallIntegerField(
        verbose_name='Балл',
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ('-score',)
