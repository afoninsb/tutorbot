"""
    Класс направления Сallback_query.
    Идет перенаправление в зависимости от полученного содержимого
    ответа callback_query.
"""

from edubot.main_classes.localdata import (
    AdminUser, StudentUser, TaskData, UserData
)
from edubot.main_classes.botdata import BotData
from .datatypesclass import Observer, Subject


class CallbackPush(Observer):
    """Нажата кнопка 'Ответить' на задание."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        if (
            subject._state != 'answer'
            or not isinstance(user, (AdminUser, StudentUser))
        ):
            return
        if kwargs['is_admin']:
            student_user = StudentUser(user.chat_id, bot.token)
        else:
            student_user = user
        task = TaskData(kwargs['callback_query'].split(':')[1])
        count = task.count_logs(student_user)
        if count > 0:
            text = 'Вы уже отвечали на этот вопрос!'
        else:
            user.edit(state=kwargs['callback_query'])
            text = 'Наберите и отправьте ваш ответ'
        answer = {
            'chat_id': user.chat_id,
            'text': text,
        }
        bot.send_answer(answer)


class CallbackReply(Observer):
    """Нажата кнопка 'Ответить' на сообщение."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        if (subject._state == 'reply'
                and isinstance(user, (AdminUser, StudentUser))):
            user.edit(state=kwargs['callback_query'])
            send_user = StudentUser(
                kwargs['callback_query'].split(':')[1], bot.token)
            answer = {
                'chat_id': user.chat_id,
                'text':
                (f'Отправьте ваш ответ (только текст). Его получит '
                 f'{send_user.full_name}'),
            }
            bot.send_answer(answer)
