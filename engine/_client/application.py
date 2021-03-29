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
        if command == SHUTDOWN:
            self._running = False

    def _update_app(self) -> None:
        self._handle_events()
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
        self._handle_commands()
        if self._initialized:
            self._update_app()
