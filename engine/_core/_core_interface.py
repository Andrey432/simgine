from .._special import Singleton
(2)
from ._core import Core


__all__ = ['CoreInterface']


class CoreInterface(Singleton):
    __slots__ = ('_core', '_initialized')

    def __init__(self):
        super().__init__()
        self._core = Core()
        self._initialized = False

    ################
    # Core         #
    ################
    def init(self):
        self._core.init()
        self._initialized = True

    def run_forever(self):
        if not self._initialized:
            raise Exception('Engine is not initialized')
        self._core.run()

    def reload_code(self):
        self._core.modules_ctrl.reload()

    def shutdown(self):
        self._core.shutdown()

    ################
    # Application  #
    ################

    def gui_events(self):
        return self._core.app_ctrl.gui

    ################
    # Scenes       #
    ################
    def create_scene(self, name):
        self._core.scenes_ctrl.create_empty_scene(name)

    def change_scene(self, name):
        self._core.scenes_ctrl.change_scene(name)

    def current_scene(self):
        return self._core.scenes_ctrl.current_scene().name
