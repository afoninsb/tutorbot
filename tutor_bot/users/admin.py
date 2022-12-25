from django.contrib import admin

from bots.admin import BotkInline
from users.models import AdminBot, Student, StudentBot


@admin.register(AdminBot)
class UserAdmin(admin.ModelAdmin):
    """Представление админов в админ-панели."""
    list_display = (
        'tgid',
        'time',
        'first_name',
        'last_name',
        'pin',
    )
    list_filter = ('time',)
    search_fields = ('tgid',)
    inlines = (BotkInline, )


@admin.register(Student)
class UserStudent(admin.ModelAdmin):
    """Представление учащихся в админ-панели."""
    list_display = (
        'tgid',
        'time',
        'first_name',
        'last_name',
    )
    list_filter = ('time', )
    search_fields = ('tgid', 'last_name')


@admin.register(StudentBot)
class UserStudentBot(admin.ModelAdmin):
    """Представление админов в админ-панели."""
    list_display = (
        'bot',
        'student',
        'is_activated',
    )
    list_filter = ('bot', 'is_activated')
    search_fields = ('bot',)
