from ._base import BaseObject
from ... import _core

__all__ = ['DataObject']


class DataObject(BaseObject):
    def __init__(self):
        super().__init__()
        self.__engine = _core.CoreInterface.instance()

    @property
    def engine(self):
        return self.__engine

    def update(self, timedelta: float) -> None:
        pass
