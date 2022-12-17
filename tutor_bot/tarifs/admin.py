from django.contrib import admin

from tarifs.models import Tarif


@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    """
    Представление тарифов в админ-панели.
    """

    list_display = (
        'id',
        'duration',
        'price',
    )
