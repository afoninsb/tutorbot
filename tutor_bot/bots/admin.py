from django.contrib import admin

from bots.models import Bot
from content.admin import CategorykInline


class BotkInline(admin.TabularInline):
    model = Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    """Представление ботов в админ-панели."""
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
    inlines = (CategorykInline, )
