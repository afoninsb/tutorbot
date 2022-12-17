

def can_category_run(category):
    permission = (1,)

    if (not category.task.filter(time__isnull=True).exists()
            and not category.is_active):
        permission = (
            2,
            'Нельзя запустить категорию. Необходимо добавить задачи!',
            'content:category_tasks'
        )

    return permission
