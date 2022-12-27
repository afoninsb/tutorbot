"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from edubot.main_classes.localdata import AdminUser, UserData
from edubot.main_classes.botdata import BotData

from .datatypesclass import Observer, Subject


class CommandCancel(Observer):
    """Отменяем текущую операцию."""
    def update(
            self, subject: Subject, bot: BotData, user: UserData
    ) -> None:
        if subject._state == 'cancel' and isinstance(user, AdminUser):
            user.edit(state='')
            answer = {
                'chat_id': user.chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)
