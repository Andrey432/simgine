from .._constants import INF
from .._math import *
from ._circle import Circle
from ._rect import Rect
from math import sqrt


__all__ = ['collision']


def _get_nearest(pivot: Vec2, first: Vec2, second: Vec2) -> Vec2:
    if (pivot - first).length_squared() < (pivot - second).length_squared():
        return first
    return second


def rect2rect(first: Rect, second: Rect) -> Vec2:
    sides = [*first.sides()]
    center = first.center
    nearest = Vec2(INF, INF)

    for i in second.sides():
        for j in sides:
            res = i.intersect(j)
            if res is not None:
                nearest = _get_nearest(center, res, nearest)
    return nearest


def rect2circle(rect, circle):
    center = rect.center
    nearest = Vec2(INF, INF)
    for i in rect.sides():
        res = line2circle(i, circle)
        if res is not None:
            nearest = _get_nearest(center, res, nearest)
    return nearest


def point2rect(point, rect):
    pass


def point2circle(point, circle):
    return (point - circle.center).length_squared() < circle.radius * circle.radius


def line2rect(line, rect):
    nearest = Vec2(INF, INF)
    origin = line.origin

    for i in rect.sides():
        res = line.intersect(i)
        if res is not None:
            nearest = _get_nearest(origin, res, nearest)
    return nearest


def line2circle(line, circle):
    oc = line.origin - circle.center
    b = oc.dot(line.direction)
    h = b * b - oc * oc + circle.radius * circle.radius
    if h < 0:
        return None

    h = sqrt(h)
    p1 = line.origin + line.direction * (-b - h)
    p2 = line.origin + line.direction * (-b + h)
    cp1, cp2 = line.contain_point(p1), line.contain_point(p2)

    if cp1 and cp2:
        return _get_nearest(line.origin, p1, p2)
    elif cp1:
        return p1
    elif cp2:
        return p2


_TABLE = {
    (Rect, Rect): rect2rect,
    (Rect, Circle): rect2circle,
    (Line, Rect): line2rect,
    (Line, Circle): line2circle,
    (Ray, Rect): line2rect,
    (Ray, Circle): line2circle,
    (Segment, Rect): line2rect,
    (Segment, Circle): line2circle,
}


def collision(first, second):
    pair = (type(first), type(second))
    if pair in _TABLE:
        return _TABLE[pair](first, second)
    return _TABLE[(type(second), type(first))](first, second)
