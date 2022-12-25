from django.contrib import admin

from content.models import Category, Log, Task


class TaskInline(admin.TabularInline):
    model = Task


class CategorykInline(admin.TabularInline):
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Представление ботов в админ-панели."""

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
    """Представление ботов в админ-панели."""

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


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """Представление лога в админ-панели."""

    list_display = (
        'student',
        'task',
        'answer',
        'is_truth',
        'time',
        'bot',
        'category',
        'score'
    )
    list_filter = ('time',)
    search_fields = ('student',)
