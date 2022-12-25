from content.models import Category
from typing import Tuple


def can_category_run(category: Category) -> Tuple[int, str]:
    """Можно ли запустить категорию?"""
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
