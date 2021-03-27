from ..shapes import _BaseShape, _T_BOUNDARY


class ObjectTransform:
    __slots__ = ('__x', '__y', '__angle', '__shape')

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__shape = None

    def boundary(self) -> _T_BOUNDARY:
        b, x, y = self.__shape.boundary(), self.__x, self.__y
        return b[0] + x, b[1] + y, b[2] + x, b[3] + y
    
    def set_shape(self, shape: _BaseShape) -> None:
        self.__shape = shape

    def rotate(self, angle: float) -> None:
        self.__angle += angle

    def set_angle(self, angle: float) -> None:
        self.__angle = angle

    def move(self, x: float, y: float) -> None:
        self.__x += x
        self.__y += y

    def move_to(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y
