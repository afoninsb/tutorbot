"""
    Классы, определяющие Наблюдателя и Подписчика,
    а также интерфейс для их взаимодействия.
"""

from abc import ABC, abstractmethod
from typing import List

from edubot.main_classes.botdata import BotData
from edubot.main_classes.localdata import LocalData


class Subject(ABC):
    """
    Интферфейс издателя объявляет набор методов для управлениями подписчиками.
    """

    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def clean(self, observer: 'Observer') -> None:
        """
        Очищает список наблюдателей издателя.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


class Road(Subject):
    """
    Издатель владеет некоторым важным состоянием и оповещает наблюдателей о его
    изменениях.
    """

    _state: int = None
    """
    Для удобства в этой переменной хранится состояние Издателя, необходимое
    всем подписчикам.
    """

    _observers: List[Observer] = []
    """Список подписчиков."""

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def clean(self, observer: Observer) -> None:
        self._observers.clear()

    def notify(self, bot: BotData, local: LocalData, **kwargs) -> None:
        """
        Запуск обновления в каждом подписчике.
        """
        for observer in self._observers:
            observer.update(self, bot, local, **kwargs)

        self.clean(observer)

    def go(self, state: str, bot: BotData, local: LocalData, **kwargs) -> None:
        """
        Получаем состояние state и запускаем оповещение всех
        прикреплённых на данный момент подписчиков.
        """
        self._state = state
        self.notify(bot, local, **kwargs)
