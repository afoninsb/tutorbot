"""
    Класс направления Сallback_query.
    Идет перенаправление в зависимости от полученного содержимого
    ответа callback_query.
"""

from django.conf import settings

from core.main_classes.botdata import BotData
from core.main_classes.localdata import AdminUser, TempUser, UserData
from regbot.keyboards.main import hide_kbrd, main_kbrd
from .datatypesclass import Observer, Subject


class CallbackApprove(Observer):
    """Одобряем заявку в админы."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        if subject._state == 'approve':
            data = kwargs['callback_query'].split(':')
            chat_id = data[1]
            text = '''Ваша заявка одобрена.

                На клавиатуре нажмите кнопу "Администрировать",
                чтобы пройти в административную панель.'''
            answer = {
                'chat_id': chat_id,
                'text': text,
                'reply_markup': main_kbrd(chat_id),
            }
            bot.send_answer(answer)
            answer_to_boss = {
                'chat_id': settings.BIG_BOSS_ID,
                'text': 'Отправлено одобрение',
            }
            bot.send_answer(answer_to_boss)
            temp_user = TempUser(chat_id)
            admin_user = AdminUser(chat_id)
            admin_user.to_base(
                tgid=chat_id,
                first_name=temp_user.firstname,
                last_name=temp_user.lastname,
            )
            temp_user.delete()


class CallbackReject(Observer):
    """Отклоняем заявку в админы."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        if subject._state == 'reject':
            data = kwargs['callback_query'].split(':')
            temp_user = TempUser(data[1])
            temp_user.delete()
            answer = {
                'chat_id': data[1],
                'text': 'Ваша заявка отклонена!',
                'reply_markup': hide_kbrd(),
            }
            bot.send_answer(answer)
            answer_to_boss = {
                'chat_id': settings.BIG_BOSS_ID,
                'text': 'Отправлен отказ',
            }
            bot.send_answer(answer_to_boss)


class CallbackReply(Observer):
    """Отвечаем на сообщение."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        if subject._state == 'reply' and kwargs['is_admin']:
            data = kwargs['callback_query'].split(':')
            user.edit(state=f'reply:{data[1]}')
            send_user_name = AdminUser(data[1]).fullname
            answer = {
                'chat_id': user.chat_id,
                'text':
                (f'Отправьте ваш ответ (только текст). Его получит '
                 f'{send_user_name}'),
            }
            bot.send_answer(answer)
