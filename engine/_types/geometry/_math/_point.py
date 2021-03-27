from .._constants import *


__all__ = ['distance2point_squared']


def distance2point_squared(segment, point) -> float:
    line = segment.move(point * -1)
    return line.c * line.c / (line.a * line.a + line.b * line.b)
