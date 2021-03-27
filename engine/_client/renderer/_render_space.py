import pygame
from . import _renderer


_T_RENDER = tuple[tuple[int, int], pygame.Surface]


class RenderSpace:
    __slots__ = ('_rect', '_surf', '_background', '_renderer')

    def __init__(self, rect: pygame.Rect, background: pygame.Color):
        self._rect = pygame.Rect(rect)
        self._surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self._background = background
        self._renderer = _renderer.Renderer(self)

    @property
    def canvas(self) -> pygame.Surface:
        return self._surf

    def change(self, rect: pygame.Rect) -> None:
        self._rect.topleft = rect.topleft
        if rect.size != self._rect.size:
            self._surf = pygame.Surface(rect.size, pygame.SRCALPHA)

    def fill(self, color: pygame.Color, rect: pygame.Rect = None) -> None:
        if rect:
            self._surf.fill(color, rect)
        else:
            self._surf.fill(color)

    def clear(self) -> None:
        self._surf.fill(self._background)

    def render(self) -> _T_RENDER:
        self._renderer.render()
        return self._rect.topleft, self._surf
