import pygame
from . import gui, renderer, window, resources
from .._special import Singleton
from .._constants.multiprocessing import *
from .._controllers import ModulesController, Config


class Application(Singleton):
    __slots__ = ('_running', '_initialized', '_controller',
                 '_gui', '_res', '_window', '_cameras',
                 '_md_controller', '_config')

    def __init__(self, controller):
        self._running = True
        self._initialized = False
        self._controller = controller

        self._gui = gui.GUIManager()
        self._cameras = []
        self._window = window.Window()
        self._res = resources.ResourcesManager()
        self._config = Config()
        self._md_controller = ModulesController()

    @property
    def config(self):
        return self._config

    @property
    def md_controller(self):
        return self._md_controller

    @property
    def gui(self):
        return self._gui

    @property
    def resources(self) -> resources.ResourcesManager:
        return self._res

    @property
    def window(self) -> window.Window:
        return self._window

    def _handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.shutdown()
        elif event.type == pygame.VIDEORESIZE:
            self._window.resize()

    def _handle_command(self, command, *args) -> None:
        if command == SHUTDOWN:
            self._running = False

    def _handle_events(self) -> None:
        for i in self._controller.read():
            self._handle_command(*i)

        if self._initialized:
            for e in pygame.event.get():
                self._handle_event(e)
                self._gui.handle_event(e)

    def _update_app(self) -> None:
        self._window.clear()
        self._gui.update()
        self._window.update()

    def init(self) -> None:
        pygame.init()
        self._config.init()
        self._md_controller.init()
        self._window.init()
        self._gui.init()
        self._initialized = True

    def is_running(self) -> bool:
        return self._running

    def shutdown(self) -> None:
        self._controller.send(SHUTDOWN)
        self._running = False

    def update(self) -> None:
        self._handle_events()
        if self._initialized:
            self._update_app()
