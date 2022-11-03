"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from .datatypesclass import Observer, Subject


class CommandCancel(Observer):
    def update(self, subject: Subject, bot, local) -> None:
        if subject._state == 'cancel':
            local.user_edit(state='')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)


class CommandSignUpToGroup(Observer):
    def update(self, subject: Subject, bot, local) -> None:
        if subject._state == 'signup_to_group':
            local.user_edit(state='to_group')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Введите пин-код группы, выданный вам учителем:',
            }
            bot.send_answer(answer)


class CommandChangeName(Observer):
    def update(self, subject: Subject, bot, local) -> None:
        if subject._state == 'change_name':
            local.user_edit(state='change_first_name')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Введите ваше Имя (только Имя и повнимательнее):',
            }
            bot.send_answer(answer)
