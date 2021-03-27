from ._vec2 import Vec2
from ._funcs import cross
from .._constants import EPS

__all__ = ['Line', 'Ray', 'Segment']


class Line:
    __slots__ = ('a', 'b', 'c', 'origin', 'direction')

    def __init__(self, start: Vec2, end: Vec2):
        self.a = start.y - end.y
        self.b = end.x - start.x
        self.c = cross(*start, *end)
        self.origin = start
        self.direction = (end - start).normalize()
    
    def _correct_point(self, point):
        return True

    def intersect(self, line: 'Line'):
        z = cross(self.a, self.b, line.a, line.b)
        if z != 0:
            point = Vec2(-cross(self.c, self.b, line.c, line.b) / z, -cross(self.a, self.c, line.a, line.c) / z)
            if self._correct_point(point) and line._correct_point(point):
                return point

    def move_to(self, point: Vec2) -> 'Line':
        return self.move(point - self.origin)

    def move(self, vector: Vec2) -> 'Line':
        return Line(self.origin + vector, self.origin + self.direction + vector)


class Ray(Line):
    def _correct_point(self, point):
        x = (abs(self.origin.x) - point.x) < EPS if abs(self.direction.x) < EPS \
            else (point.x > self.origin.x - EPS) == (self.direction.x > 0)
        y = (abs(self.origin.y) - point.y) < EPS if abs(self.direction.y) < EPS \
            else (point.y > self.origin.y - EPS) == (self.direction.y > 0)
        return x and y
    
    def contain_point(self, point):
        return self._correct_point(point)

    def move(self, vector) -> 'Ray':
        return Ray(self.origin + vector, self.origin + self.direction + vector)


class Segment(Ray):
    __slots__ = ('end',)

    def __init__(self, start: Vec2, end: Vec2):
        super().__init__(start, end)
        self.end = end
    
    def _correct_point(self, point):
        xmin, xmax = min(self.origin.x, self.end.x), max(self.origin.x, self.end.x)
        ymin, ymax = min(self.origin.y, self.end.y), max(self.origin.y, self.end.y)
        return xmin - EPS < point.x < xmax + EPS \
               and ymin - EPS < point.y < ymax + EPS

    def move(self, vector: Vec2) -> 'Segment':
        return Segment(self.origin + vector, self.end + vector)
