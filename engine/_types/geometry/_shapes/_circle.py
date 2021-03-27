from .._math import Vec2


class Circle:
    __slots__ = ('radius', 'center')

    def __init__(self, center: Vec2, radius: float):
        self.radius = radius
        self.center = Vec2(center)
