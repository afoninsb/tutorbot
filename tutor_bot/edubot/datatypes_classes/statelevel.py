"""
    Класс направления Состояние юзера.
    Идет перенаправление в зависимости от полученного состояния юзера.
"""

from .datatypesclass import Observer, Subject
from .states import change_name, exchange_message, push, registration


class StateDistributor(Observer):
    def update(self, subject: Subject, bot, user, **kwargs) -> None:
        """Направления при наличии состояния."""
        pathes = {
            'start': registration.reg_start,
            'password': registration.reg_password,
            'first_name': registration.reg_first_name,
            'last_name': registration.reg_last_name,
            'change_first_name': change_name.change_first_name,
            'change_last_name': change_name.change_last_name,
            'message_to_teacher': exchange_message.message_to_admin,
            'reply': exchange_message.reply,
            'answer': push.answer,
        }
        state = subject._state.split(':')[0]
        if state in pathes:
            pathes[state](
                kwargs['message'],
                bot,
                user,
                is_admin=kwargs['is_admin']
            )
