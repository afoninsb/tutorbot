"""
    Класс направлений верхнего уровня.
    Идет перенаправление в зависимости от получения одного из 4 состояний:
    - Состояние юзера;
    - Команда;
    - Callback_query;
    - Текст.
"""

from edubot.main_classes import BotData, UserData

from .datatypesclass import Observer, Road, Subject


class HighLevelCommand(Observer):
    def update(
        self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        """Направления при получении комманды."""
        from .commandlevel import CommandCancel, CommandChangeName
        if subject._state == 'command':
            command = kwargs['message']['text']
            road = Road()
            pathes = (
                CommandCancel(),
                CommandChangeName(),
            )
            for path in pathes:
                road.attach(path)
            road.go(command, bot, user)


class HighLevelCallback(Observer):
    def update(
        self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        """Направления при получении callback_query."""
        from .callbacklevel import CallbackPush, CallbackReply
        if subject._state == 'callback_query':
            callback_query = kwargs['from_tg']['callback_query']['data']
            callback = callback_query.split(':')[0]
            road = Road()
            pathes = (
                CallbackPush(),
                CallbackReply(),
            )
            for path in pathes:
                road.attach(path)
            road.go(callback, bot, user, callback_query=callback_query, is_admin=kwargs['is_admin'])


class HighLevelText(Observer):
    def update(
        self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        """Направления при получении обычного текста."""
        from .textlevel import (TextGoToPanel, TextHaHaHa,
                                TextMessageToTeacher, TextMyStat)
        if subject._state == 'text':
            text = bot.get_message(kwargs['from_tg'])['text']
            road = Road()
            pathes = (
                TextMessageToTeacher(),
                TextGoToPanel(),
                TextMyStat(),
                TextHaHaHa(),
            )
            for path in pathes:
                road.attach(path)
            road.go(text, bot, user, is_admin=kwargs['is_admin'])


class HighLevelState(Observer):
    def update(
        self, subject: Subject, bot: BotData, user: UserData, **kwargs
    ) -> None:
        """Направления, если юзер в каком-либо состоянии."""
        from .statelevel import StateDistributor
        if subject._state == 'state':
            state = user.get_info.state
            road = Road()
            pathes = (
                StateDistributor(),
            )
            for path in pathes:
                road.attach(path)
            road.go(
                state, bot, user,
                message=kwargs['message'],
                is_admin=kwargs['is_admin']
            )
