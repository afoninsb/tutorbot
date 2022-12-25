from typing import Any
from django.template.defaulttags import register


@register.filter
def get_item(dictionary: dict, key: int) -> Any:
    """Получаем значение словаря по ключу."""
    return dictionary.get(key)
