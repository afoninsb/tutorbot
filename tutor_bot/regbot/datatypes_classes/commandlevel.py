"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from .datatypesclass import Observer, Subject


class CommandCancel(Observer):
    def update(self, subject: Subject, bot, user) -> None:
        if subject._state == 'cancel':
            user.edit(state='')
            answer = {
                'chat_id': user.chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)
