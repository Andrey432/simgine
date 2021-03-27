from ._vec2 import Vec2

__all__ = ['cross', 'get_normal']


def cross(x_1: float, y_1: float, x_2: float, y_2: float) -> float:
    return x_1 * y_2 - x_2 * y_1


def get_normal(line) -> Vec2:
    return Vec2(line.a, line.b)
