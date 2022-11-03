"""
    Класс направлений верхнего уровня.
    Идет перенаправление в зависимости от получения одного из 4 состояний:
    - Состояние юзера;
    - Команда;
    - Callback_query;
    - Текст.
"""

from edubot.main_classes import BotData, LocalData

from .datatypesclass import Observer, Road, Subject


class HighLevelCommand(Observer):
    def update(
        self, subject: Subject, bot: BotData, local: LocalData, **kwargs
    ) -> None:
        """Направления при получении комманды."""
        from .commandlevel import (CommandCancel, CommandChangeName,
                                   CommandSignUpToGroup)
        if subject._state == 'command':
            command = kwargs['message']['text'][1:]
            road = Road()
            pathes = (
                CommandCancel(),
                CommandChangeName(),
                CommandSignUpToGroup()
            )
            for path in pathes:
                road.attach(path)
            road.go(command, bot, local)


class HighLevelCallback(Observer):
    def update(
        self, subject: Subject, bot: BotData, local: LocalData, **kwargs
    ) -> None:
        """Направления при получении callback_query."""
        from .callbacklevel import CallbackItem, CallbackPush, CallbackReply
        if subject._state == 'callback_query':
            callback_query = kwargs['from_tg']['callback_query']['data']
            callback = callback_query.split(':')[0]
            road = Road()
            pathes = (
                CallbackItem(),
                CallbackPush(),
                CallbackReply(),
            )
            for path in pathes:
                road.attach(path)
            road.go(callback, bot, local, callback_query=callback_query)


class HighLevelText(Observer):
    def update(
        self, subject: Subject, bot: BotData, local: LocalData, **kwargs
    ) -> None:
        """Направления при получении обычного текста."""
        from .textlevel import (TextGoToPanel, TextHaHaHa, TextMessageToAdmins,
                                TextMessageToTeacher, TextPlan, TextSupport)
        if subject._state == 'text':
            text = bot.get_message(kwargs['from_tg'])['text']
            road = Road()
            pathes = (
                TextPlan(),
                TextMessageToTeacher(),
                TextGoToPanel(),
                TextHaHaHa(),
                TextMessageToAdmins(),
                TextSupport(),
            )
            for path in pathes:
                road.attach(path)
            road.go(text, bot, local)


class HighLevelState(Observer):
    def update(
        self, subject: Subject, bot: BotData, local: LocalData, **kwargs
    ) -> None:
        """Направления, если юзер в каком-либо состоянии."""
        from .statelevel import StateDistributor
        if subject._state == 'state':
            state = local.user_state
            road = Road()
            pathes = (
                StateDistributor(),
            )
            for path in pathes:
                road.attach(path)
            road.go(state, bot, local, message=kwargs['message'])
