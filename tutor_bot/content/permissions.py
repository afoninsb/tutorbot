

def can_category_run(category):
    return (
        (
            2,
            'Нельзя запустить категорию. Необходимо добавить задачи!',
            'content:category_tasks',
        )
        if (
            not category.task.filter(time__isnull=True).exists()
            and not category.is_active
        )
        else (1,)
    )
