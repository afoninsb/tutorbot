"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from edubot.main_classes.localdata import AdminUser, StudentUser

from .datatypesclass import Observer, Subject


class CommandCancel(Observer):
    """Команда 'Отменить текущую операцию'."""
    def update(self, subject: Subject, bot, user) -> None:
        if (subject._state == 'cancel'
                and isinstance(user, (AdminUser, StudentUser))):
            user.edit(state='')
            answer = {
                'chat_id': user.chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)


class CommandChangeName(Observer):
    """Команда 'Изменить имя и фамилию'."""
    def update(self, subject: Subject, bot, user) -> None:
        if (subject._state == 'change_name'
                and isinstance(user, (AdminUser, StudentUser))):
            user.edit(state='change_first_name')
            answer = {
                'chat_id': user.chat_id,
                'text': 'Введите ваше Имя (только Имя и повнимательнее):',
            }
            bot.send_answer(answer)
