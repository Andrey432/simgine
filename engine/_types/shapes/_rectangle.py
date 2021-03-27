from ._shapes_base import *


class RectShape(_BaseShape):
    def __init__(self, width: float, height: float, angle: float):
        super().__init__()
        self.__w = width
        self.__h = height
        self.__a = angle

    @property
    def width(self):
        return self.__w

    @property
    def height(self):
        return self.__h

    @property
    def angle(self):
        return self.__a

    def resize(self, width: float, height: float) -> None:
        self.__w = width
        self.__h = height

    def scale(self, scale: float) -> None:
        self.__w *= scale
        self.__h *= scale

    def rotate(self, angle: float) -> None:
        self.__a = angle

    def boundary(self) -> _T_BOUNDARY:
        pass
