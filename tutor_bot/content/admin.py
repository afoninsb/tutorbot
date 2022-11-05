from django.contrib import admin

from content.models import Category, Task


class TaskInline(admin.TabularInline):
    model = Task


class CategorykInline(admin.TabularInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Представление ботов в админ-панели.
    """

    list_display = (
        'name',
        'is_active',
        'bot',
    )
    list_filter = ('is_active', 'bot')
    search_fields = ('name',)
    inlines = (TaskInline,)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Представление ботов в админ-панели.
    """

    list_display = (
        'title',
        'text',
        'answer',
        'img',
        'time',
        'bot',
        'category',
    )
    list_filter = ('time', 'bot', 'category')
    search_fields = ('text',)
