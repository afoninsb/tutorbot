"""
    Класс направления Состояние юзера.
    Идет перенаправление в зависимости от полученного состояния юзера.
"""

from .datatypesclass import Observer, Subject
from .states import exchange_message, registration


class StateDistributor(Observer):
    """Направления, если пользователь в каком-то состоянии."""
    def update(self, subject: Subject, bot, user, **kwargs) -> None:
        pathes_temp_admin = {
            'start': registration.reg_start,
            'get_admin_first_name': registration.reg_first_name,
            'get_admin_last_name': registration.reg_last_name,
            'get_admin_org': registration.reg_org,
            'get_admin_position': registration.reg_position,
            'get_admin_why': registration.reg_why,
        }
        pathes_admin = {
            'message_to_admins': exchange_message.message_to_admins,
            'support': exchange_message.support,
            'reply': exchange_message.reply,
        }
        state = subject._state.split(':')[0]
        if kwargs['is_admin'] and state in pathes_admin:
            pathes_admin[state](kwargs['message'], bot, user)
        elif not kwargs['is_admin'] and state in pathes_temp_admin:
            pathes_temp_admin[state](kwargs['message'], bot, user)
