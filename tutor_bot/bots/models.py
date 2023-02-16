from datetime import datetime
from django.db import models
from django.utils import timezone

from tarifs.models import Tarif
from users.models import AdminBot


class Bot(models.Model):
    """Модель бота."""
    class DayType(models.TextChoices):
        """Дни раздачи заданий."""
        WORKING_DAYS = 'WORKING_DAYS', 'Рабочие дни'
        WEEK_DAYS = 'WEEK', 'Вся неделя'

    class TimeZones(models.TextChoices):
        """Часовые пояса России."""
        KALININGRAD = 'Europe/Kaliningrad', 'Europe/Kaliningrad +02'
        MOSCOW = 'Europe/Moscow', 'Europe/Moscow +03'
        SAMARA = 'Europe/Samara', 'Europe/Samara +04'
        YEKATERINBURG = 'Asia/Yekaterinburg', 'Asia/Yekaterinburg +05'
        OMSK = 'Asia/Omsk', 'Asia/Omsk +06'
        KRASNOYARSK = 'Asia/Krasnoyarsk', 'Asia/Krasnoyarsk +07'
        IRKUTSK = 'Asia/Irkutsk', 'Asia/Irkutsk +08'
        CHITA = 'Asia/Chita', 'Asia/Chita +09'
        VLADIVOSTOK = 'Asia/Vladivostok', 'Asia/Vladivostok +10'
        MAGADAN = 'Asia/Magadan', 'Asia/Magadan +11'
        KAMCHATKA = 'Asia/Kamchatka', 'Asia/Kamchatka +12'

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
        max_length=500
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
    is_show_wrong_right = models.BooleanField(
        verbose_name='Показывать Правильно-Неправильно?',
        default=True
    )
    is_show_answer = models.BooleanField(
        verbose_name='Показывать правильный ответ?',
        default=True
    )
    tz = models.CharField(
        verbose_name='Часовой пояс',
        max_length=20,
        choices=TimeZones.choices,
        default=TimeZones.MOSCOW
    )
    tarif = models.ForeignKey(
        Tarif,
        verbose_name='Тариф',
        on_delete=models.CASCADE,
        related_name='bot',
    )
    start_time = models.DateTimeField(
        verbose_name='Дата начала тарифа',
        default=timezone.now,
    )
    end_time = models.DateTimeField(
        verbose_name='Дата конца тарифа',
        default=datetime(2100, 12, 31)
    )
    is_paid = models.BooleanField(
        verbose_name='Оплачено?',
        default=False
    )
    last_rating = models.CharField(
        verbose_name='Дата последнего рейтинга',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    def __str__(self):
        return f'Бот "{self.name}": {self.login}'
