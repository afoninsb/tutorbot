from django.db import models


class Tarif(models.Model):
    """Модель тарифов."""

    class TarifsTypes(models.IntegerChoices):
        FREE = 0, 'бессрочно'
        ONE = 1, '1 месяц'
        THREE = 3, '3 месяца'
        FIVE = 5, '5 месяцев'
        NINE = 9, '9 месяцев'
        TEN = 10, '10 месяцев'

    duration = models.PositiveSmallIntegerField(
        verbose_name='Тарифы',
        choices=TarifsTypes.choices,
        unique=True
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Стоимость тарифа',
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return f'{self.duration} мес.: {self.price} руб.'
