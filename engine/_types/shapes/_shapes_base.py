from abc import ABC, abstractmethod

__all__ = ['_BaseShape', '_T_BOUNDARY']


_T_BOUNDARY = tuple[float, float, float, float]


class _BaseShape(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def resize(self, *args) -> None:
        pass

    @abstractmethod
    def rotate(self, angle: float) -> None:
        pass

    @abstractmethod
    def scale(self, scale: float) -> None:
        pass

    @abstractmethod
    def boundary(self) -> _T_BOUNDARY:
        pass
