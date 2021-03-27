import pygame
from . import gui, renderer, _window, _resources
from .._special import Singleton
from .._constants.multiprocessing import *


class Application(Singleton):
    __slots__ = ('_running', '_initialized', '_controller', '_gui', '_res', '_window', '_cameras')

    def __init__(self, controller):
        self._running = True
        self._initialized = False
        self._controller = controller

        self._gui = gui.GUIManager()
        self._cameras = []
        self._window = _window.Window()
        self._res = _resources.ResourcesManager()

    @property
    def resources(self) -> _resources.ResourcesManager:
        return self._res

    @property
    def window(self) -> _window.Window:
        return self._window

    @property
    def running(self) -> bool:
        return self._running

    def _init(self, settings) -> None:
        pygame.init()
        self._window.init(settings)
        self._gui.init(settings)
        self._initialized = True

    def _handle_sys_event(self, event: pygame.event.Event) -> [None, tuple]:
        self._gui.handle_event(event)
        if event.type == pygame.QUIT:
            self.shutdown()
            return
        elif event.type == pygame.VIDEORESIZE:
            self._window.resize()

    def _handle_events(self) -> None:
        gui_h = self._gui.handle_event
        sys_h = self._handle_sys_event

        for e in pygame.event.get():
            handler = gui_h if e.type == pygame.USEREVENT else sys_h
            # noinspection PyArgumentList
            response = handler(e)
            if response:
                self._controller.send(GUI_EVENT, *response)

    def _handle_commands(self) -> None:
        for i in self._controller.read():
            self._handle_command(*i)

    def _handle_command(self, command, *args) -> None:
        if command == STARTUP:
            self._init(*args)
        elif command == SHUTDOWN:
            self._running = False

    def _update_app(self) -> None:
        self._handle_events()
        self._window.clear()
        self._gui.update()
        self._window.update()

    def shutdown(self) -> None:
        self._controller.send(SHUTDOWN)
        self._running = False

    def update(self) -> None:
        self._handle_commands()
        if self._initialized:
            self._update_app()
