from django.db import models


class AdminBot(models.Model):
    """Модель администратора ботов."""

    tgid = models.CharField(
        verbose_name='Telegram ID',
        max_length=20,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20
    )
    time = models.DateTimeField(
        verbose_name='Last login time',
        auto_now=True
    )
    pin = models.CharField(
        max_length=50,
        blank=True
    )
    state = models.CharField(
        max_length=50,
        blank=True
    )

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ('last_name',)

    def __str__(self):
        return f'{self.tgid}: {self.last_name} {self.first_name}'


class Student(models.Model):
    """Модель учащихся."""

    from bots.models import Bot

    tgid = models.CharField(
        verbose_name='Telegram ID',
        max_length=20,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20
    )
    time = models.DateTimeField(
        verbose_name='Last login time',
        auto_now=True
    )
    state = models.CharField(
        max_length=50,
        blank=True
    )
    bot = models.ManyToManyField(
        Bot,
        through="StudentBot"
    )

    class Meta:
        verbose_name = 'Учащийся'
        verbose_name_plural = 'Учащиеся'
        ordering = ('last_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class StudentBot(models.Model):
    """Связь учащихся с ботами."""

    from bots.models import Bot

    bot = models.ForeignKey(
        Bot,
        verbose_name='Бот',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        verbose_name='Учащийся',
        on_delete=models.CASCADE,
    )
    is_activated = models.BooleanField(
        verbose_name='Активирован?',
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('bot', 'student'), name='unique_StudentBot')
        ]
