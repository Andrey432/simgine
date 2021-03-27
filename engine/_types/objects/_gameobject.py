from ._base import BaseObject
from ._transform import ObjectTransform

__all__ = ['GameObject']


class GameObject(BaseObject):
    def __init__(self):
        super().__init__()
        self.__transform = ObjectTransform()

    @property
    def transform(self):
        return self.__transform
