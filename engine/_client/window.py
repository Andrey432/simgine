from .._controllers import Config
from functools import reduce
from pygame import display
import pygame


class Window:
    __slots__ = ('_surf', '_fps', '_flags', '_frame_rate', '_frame_time', '_background')

    def __init__(self):
        super().__init__()
        self._surf = None
        self._fps = None
        self._flags = None
        self._background = None  # type: [None, pygame.Color]
        self._frame_rate = 0
        self._frame_time = 0

    def frame_time(self):
        return self._frame_time

    def init(self):
        settings = Config.instance().get('application')
        self._flags = reduce(lambda c, v: c | getattr(pygame, v.upper()), [0] + settings["flags"])
        display.set_caption(settings.get("caption", ""))

        self._surf = display.set_mode(settings["resolution"], self._flags)
        self._fps = pygame.time.Clock()
        self._frame_rate = settings.get('fps', 0)
        self._background = pygame.Color(settings.get('background', 'black'))

    def resize(self):
        self._surf = display.get_surface()

    def canvas(self):
        return self._surf

    def clear(self):
        self._surf.fill(self._background)

    def update(self):
        pygame.display.set_caption(str(pygame.mouse.get_pos()))
        pygame.display.update()
        self._frame_time = self._fps.tick(self._frame_rate) / 1000
