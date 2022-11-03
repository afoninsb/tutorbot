from django.db import models


class Temp(models.Model):
    tgid = models.BigIntegerField(
        unique=True)
    first_name = models.CharField(
        max_length=50)
    last_name = models.CharField(
        max_length=50)
    org = models.CharField(
        max_length=500)
    position = models.CharField(
        max_length=100)
    why = models.CharField(
        max_length=1000)
    state = models.CharField(
        max_length=50,
        blank=True
    )
