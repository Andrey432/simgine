from ._shapes_base import *
from math import sqrt


class CircleShape(_BaseShape):
    __slots__ = ('__r', '__sq_r')

    def __init__(self, radius: float):
        super().__init__()
        self.__r = radius
        self.__sq_r = sqrt(radius)

    @property
    def radius(self):
        return self.__r

    def resize(self, radius: float) -> None:
        self.__r = radius
        self.__sq_r = sqrt(radius)

    def rotate(self, angle: float) -> None:
        pass

    def scale(self, scale: float) -> None:
        self.__r *= scale
        self.__sq_r = sqrt(self.__r)

    def boundary(self) -> _T_BOUNDARY:
        sqr = self.__sq_r
        return -sqr, -sqr, sqr, sqr
