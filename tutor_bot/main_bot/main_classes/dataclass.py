from abc import ABC, abstractmethod


class DataClass(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass


class Context():
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, strategy: DataClass) -> None:

        self._strategy = strategy

    @property
    def strategy(self) -> DataClass:

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: DataClass) -> None:

        self._strategy = strategy
