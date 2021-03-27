from .._math import Vec2, Segment


class Rect:
    __slots__ = ('size', 'center', 'angle',
                '_hsize', '_hsize_len', '_sides', '_points', '_deprecated')

    def __init__(self, size: Vec2, center: Vec2, angle: float):
        self.size = Vec2(size)
        self.center = Vec2(center)
        self.angle = angle

        self._hsize = self.size / 2
        self._hsize_len = self._hsize.length()
        self._sides = None
        self._points = None
        self._deprecated = True

    def _update(self):
        self._hsize = self.size / 2
        self._hsize_len = self._hsize.length()
        self._points = self._gen_points(Vec2(), self._hsize, self.angle)
        self._sides = self._gen_sides(self._points)
        self._deprecated = False

    @staticmethod
    def _gen_points(pivot: Vec2, hsize: Vec2, angle: float):
        diag_2 = Vec2(-hsize.x, hsize.y)
        hsize = hsize.rotate(angle)
        diag_2.rotate_ip(angle)
        return pivot + hsize, pivot + diag_2, pivot - hsize, pivot - diag_2

    @staticmethod
    def _gen_sides(points):
        return tuple(Segment(points[i], points[i - 1]) for i in range(4))

    def rotate(self, angle: float) -> None:
        self.angle += angle
        self._deprecated = True

    def resize(self, size: Vec2):
        self.size = size
        self._deprecated = True

    def move(self, position: Vec2) -> None:
        self.center = position

    def sides(self):
        if self._deprecated:
            self._update()
        return (i.move(self.center) for i in self._sides)

    def points(self):
        if self._deprecated:
            self._update()
        return (i + self.center for i in self._points)
