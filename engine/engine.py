from ._controllers import *
from ._special import Singleton

__all__ = ['Engine']


class Engine(Singleton):
    __slots__ = ('_config', '_modules_ctrl', '_prefabs_ctrl', '_scenes_ctrl', '_app_ctrl', '_core', '_initialized')

    def __init__(self):
        super().__init__()
        self._config = Config()
        self._initialized = False
        self._modules_ctrl = ModulesController()
        self._prefabs_ctrl = PrefabsController()
        self._scenes_ctrl = ScenesController()
        self._app_ctrl = ApplicationController()

    def _run(self):
        app = self._app_ctrl
        scenes = self._scenes_ctrl
        while app.is_running():
            scenes.update()
            app.update()
        app.join_app_proc()

    def init(self):
        self._config.init()
        self._modules_ctrl.init()
        self._app_ctrl.init()
        self._prefabs_ctrl.init()
        self._scenes_ctrl.init()
        self._initialized = True

    def run(self):
        if not self._initialized:
            raise Exception('Engine is not initialized')
        self._run()

    def shutdown(self):
        self._app_ctrl.shutdown()

    def create_scene(self, name):
        self._core.scenes_ctrl.create_empty_scene(name)

    def change_scene(self, name):
        self._scenes_ctrl.change_scene(name)

    def current_scene(self):
        return self._core.scenes_ctrl.current_scene().name

    def reload_code(self):
        self._modules_ctrl.reload()
