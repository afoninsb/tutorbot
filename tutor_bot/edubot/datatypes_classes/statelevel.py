"""
    Класс направления Состояние юзера.
    Идет перенаправление в зависимости от полученного состояния юзера.
"""

from .datatypesclass import Observer, Subject
from .states import change_name, exchange_message, push, registration, to_group


class StateDistributor(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        pathes = {
            'start': registration.reg_start,
            'password': registration.reg_password,
            'first_name': registration.reg_first_name,
            'last_name': registration.reg_last_name,
            'to_group': to_group.user_to_group,
            'change_first_name': change_name.change_first_name,
            'change_last_name': change_name.change_last_name,
            'message_to_teacher': exchange_message.message_to_admin,
            'message_to_admins': exchange_message.message_to_admins,
            'support': exchange_message.support,
            'reply': exchange_message.reply,
            'push': push.push_work,
        }
        state = subject._state.split(':')[0]
        if state in pathes:
            pathes[state](kwargs['message'], bot, local)
