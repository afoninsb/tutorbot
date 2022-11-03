"""
    Класс направления Текст.
    Идет перенаправление в зависимости от полученного текста.
"""

from uuid import uuid1

from bots.models import Bot, BotAdmin
from edubot.keyboards import admin_kbrd, main_kbrd, plans_kbrd
from edubot.main_classes import BotData, LocalData
from groups.models import Spisok
from plans.models import Plan

from .datatypesclass import Observer, Subject


class TextPlan(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'План':
            cur_bot = Bot.objects.get(tg=bot.token)
            cur_user = Spisok.objects.get(chat=local.chat_id)
            groups = cur_user.groupuser.filter(bot=cur_bot)
            plans_info = []
            for group in groups:
                plans = Plan.objects.filter(groupplan=group)
                plans_temp = []
                if plans:
                    for plan in plans:
                        plans_temp.append({'id': plan.id, 'name': plan.name})
                    plans_info.append(
                        {'group_id': group.id,
                         'group_name': group.name,
                         'plans': plans_temp}
                    )
            answer = {
                'chat_id': local.chat_id,
                'text': 'Для вас нет плана.',
            }
            if plans_info:
                answer['text'] = 'Выберите тему для работы:'
                answer['reply_markup'] = plans_kbrd(plans_info)
            bot.send_answer(answer)


class TextMessageToTeacher(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Сообщение учителю':
            local.user_edit(state='message_to_teacher')
            admins = local.admins
            number = len(admins)
            text = 'Ваше сообщение получ' + ('ит ' if number == 1 else 'ат:\n')
            for admin in admins.values():
                text += admin
                text += '\n'
            answer = {
                'chat_id': local.chat_id,
                'text': f'{text}Пишите (только текст):'
            }
            bot.send_answer(answer)


class TextMessageToAdmins(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Сообщение админам':
            local.user_edit(state='message_to_admins')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Пишите (только текст):'
            }
            bot.send_answer(answer)


class TextSupport(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Техподдержка':
            local.user_edit(state='support')
            answer = {
                'chat_id': local.chat_id,
                'text': '''Сообщите, о каком боте идет речь и суть проблемы.
                Пишите сообщение в техподдержку (только текст):'''
            }
            bot.send_answer(answer)


class TextGoToPanel(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Администрировать':
            pin = str(uuid1())
            BotAdmin.objects.filter(chat=local.chat_id).update(pin=pin)
            answer = {
                'chat_id': local.chat_id,
                'text': 'Для входа в админпанель нажмите кнопку:',
                'reply_markup': admin_kbrd(local.chat_id, pin),
            }
            bot.send_answer(answer)


class TextHaHaHa(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state not in [
                'План', 'Сообщение учителю', 'Администрировать',
                'Сообщение админам', 'Техподдержка']:
            answer = {
                'chat_id': local.chat_id,
                'text': 'Ага... и вам приветик!',
                'reply_markup': main_kbrd(local.chat_id),
            }
            bot.send_answer(answer)
