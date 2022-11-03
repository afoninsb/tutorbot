from django.contrib import admin

from bots.models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    """
    Представление ботов в админ-панели.
    """

    list_display = (
        'id',
        'login',
        'name',
        'admin',
        'is_active',
        'days',
        'hours',
    )
    list_filter = ('is_active',)
    search_fields = ('id', 'name', 'login')
