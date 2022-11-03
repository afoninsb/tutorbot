from django.db import models

from users.models import AdminBot


class Bot(models.Model):

    class DayType(models.TextChoices):
        WORKING_DAYS = 'WORKING_DAYS', 'Рабочие дни'
        WEEK_DAYS = 'WEEK', 'Вся неделя'

    token = models.CharField(
        verbose_name='Telegram token',
        max_length=100,
        unique=True
    )
    login = models.CharField(
        verbose_name='Telegram username',
        max_length=100,
        unique=True
    )
    name = models.CharField(
        verbose_name='Имя бота',
        max_length=100
    )
    is_active = models.BooleanField(
        verbose_name='Активен?',
        default=False
    )
    admin = models.ForeignKey(
        AdminBot,
        verbose_name='Администратор',
        on_delete=models.CASCADE,
        related_name='bot'
    )
    password = models.CharField(
        verbose_name='Пароль бота',
        max_length=50
    )
    days = models.CharField(
        verbose_name='Дни работы',
        max_length=20,
        choices=DayType.choices,
        default=DayType.WEEK_DAYS
    )
    hours = models.CharField(
        verbose_name='Часы запуска',
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    def __str__(self):
        return f'Бот "{self.name}": {self.login}'
