from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def move(self, to) -> None:
        pass

    @abstractmethod
    def move_relative(self, shift) -> None:
        pass

    @abstractmethod
    def rotate(self, angle) -> None:
        pass

    @abstractmethod
    def rotate_relative(self, angle) -> None:
        pass
