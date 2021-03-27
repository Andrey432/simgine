from abc import ABC, abstractmethod

__all__ = ['BaseObject']


class BaseObject(ABC):
    _id_counter = 0
    __slots__ = ('__id',)

    def __init__(self):
        super().__init__()
        self.__id = BaseObject._id_counter
        BaseObject._id_counter += 1

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def update(self, timedelta: float) -> None:
        pass
