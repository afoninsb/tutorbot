from django.contrib import admin

from regbot.models import Temp

@admin.register(Temp)
class UserAdmin(admin.ModelAdmin):
    """
    Представление админов в админ-панели.
    """

    list_display = (
        'tgid',
        'first_name',
        'last_name',
        'state'
    )
