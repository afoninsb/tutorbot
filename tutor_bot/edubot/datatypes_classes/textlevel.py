"""
    Класс направления Текст.
    Идет перенаправление в зависимости от полученного текста.
"""

from uuid import uuid1

from edubot.keyboards import admin_kbrd, hide_kbrd, main_kbrd, userstat_kbr
from edubot.main_classes import BotData, UserData
from edubot.main_classes.localdata import AdminUser, StudentUser, TempUser

from .datatypesclass import Observer, Subject


class TextMessageToTeacher(Observer):
    def update(self, subject: Subject, bot: BotData, user: UserData, **kwargs) -> None:
        if (subject._state == 'Сообщение учителю'
                and isinstance(user, StudentUser)):
            user.edit(state='message_to_teacher')
            teacher = user.teacher
            text = (f'Ваше сообщение получит '
                    f'{teacher.last_name} {teacher.first_name}. ')
            answer = {
                'chat_id': user.chat_id,
                'text': f'{text}Пишите (только текст):',
                'reply_markup': main_kbrd(user.chat_id, kwargs['is_admin']),
            }
            bot.send_answer(answer)


class TextGoToPanel(Observer):
    def update(self, subject: Subject, bot: BotData, user: UserData, **kwargs) -> None:
        if (subject._state == 'Администрировать'
                and isinstance(user, AdminUser)):
            pin = str(uuid1())
            user.edit(pin=pin)
            answer = {
                'chat_id': user.chat_id,
                'text': 'Для входа в админпанель нажмите кнопку:',
                'reply_markup': admin_kbrd(user.chat_id, pin),
            }
            bot.send_answer(answer)


class TextMyStat(Observer):
    def update(self, subject: Subject, bot: BotData, user: UserData, **kwargs) -> None:
        if subject._state == 'Моя статистика':
            pin = str(uuid1())
            user = StudentUser(user.chat_id, bot.token)
            user.edit(pin=pin)
            answer = {
                'chat_id': user.chat_id,
                'text': 'Для просмотра статистики нажмите кнопку:',
                'reply_markup': userstat_kbr(bot.bot_id, user.user_id, pin),
            }
            bot.send_answer(answer)


class TextRating(Observer):
    def update(self, subject: Subject, bot: BotData, user: UserData, **kwargs) -> None:
        if subject._state != 'Рейтинг':
            return
        user = StudentUser(user.chat_id, bot.token)
        if rating := user.get_rating:
            text = 'Вы в рейтинге\n'
            for rtng in rating:
                if rtng[0] == str(user.chat_id):
                    text = f'{text}\n{rtng[1]}. Вы - {rtng[2]}'
                else:
                    text = f'{text}\n{rtng[1]}. Ученик - {rtng[2]}'
            text = f'{text}\n\nРейтинг обновляется в 3 часа по местному времени.'
        else:
            text = 'Рейтинг сформируется в 3 часа'
        answer = {
            'chat_id': user.chat_id,
            'text': text,
        }
        bot.send_answer(answer)


class TextHaHaHa(Observer):
    def update(self, subject: Subject, bot: BotData, user: UserData, **kwargs) -> None:
        if subject._state not in [
                'Сообщение учителю', 'Администрировать',
                'Техподдержка', 'Моя статистика', 'Рейтинг']:
            answer = {
                'chat_id': user.chat_id,
                'text': 'Ага... и вам приветик!',
                'reply_markup': main_kbrd(user.chat_id, kwargs['is_admin']),
            }
            if isinstance(user, TempUser):
                answer['reply_markup'] = hide_kbrd()
            bot.send_answer(answer)
