"""
    Класс направления Сallback_query.
    Идет перенаправление в зависимости от полученного содержимого
    ответа callback_query.
"""

from edubot.keyboards import items_kbrd
from groups.models import Spisok
from plans.models import Plan

from .datatypesclass import Observer, Subject


class CallbackItem(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'item':
            data = kwargs['callback_query'].split(':')
            plan = Plan.objects.get(id=data[2])
            items = plan.plan_item.all().order_by('weight')
            text = f'''
                <b>План: {data[1]}</b>
                Выберите тему для работы:
            '''
            answer = {
                'chat_id': local.chat_id,
                'text': text,
                'reply_markup': items_kbrd(local, items, data[3]),
                'parse_mode': 'HTML'
            }
            bot.send_answer(answer)


class CallbackPush(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'push':
            data = kwargs['callback_query'].split(':')
            state = f'push:{data[1]}:{data[2]}:{data[3]}'
            if len(data) == 5:
                state += f':{data[4]}'
            local.user_edit(state=state)
            answer = {
                'chat_id': local.chat_id,
                'text': ('Отправьте ссылку на свою работу '
                         'или документ с вашей работой:'),
            }
            bot.send_answer(answer)


class CallbackReply(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'reply':
            data = kwargs['callback_query'].split(':')
            local.user_edit(state=f'{data[0]}:{data[1]}')
            send_user = Spisok.objects.get(chat=data[1])
            answer = {
                'chat_id': local.chat_id,
                'text':
                (f'Отправьте ваш ответ (только текст). Его получит '
                 f'{send_user.first_name} {send_user.last_name}'),
            }
            bot.send_answer(answer)
