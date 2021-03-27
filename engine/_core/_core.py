from .._controllers import *
(3)
from .._config import Config
from .._constants.base import *


class Core:
    # __slots__ = ('_running', 'config', 'scenes', 'time_controller')

    def __init__(self):
        self.config = Config(CONFIG_FILE)
        self.modules_ctrl = ModulesController()
        self.prefabs_ctrl = PrefabsController()
        self.scenes_ctrl = ScenesController()
        self.app_ctrl = ApplicationController()
    
    def init(self):
        self.modules_ctrl.load()
        self.prefabs_ctrl.init()
        self.scenes_ctrl.init()
        self.app_ctrl.init()

    def shutdown(self):
        self.app_ctrl.shutdown()

    def run(self):
        app = self.app_ctrl
        scenes = self.scenes_ctrl

        while app.is_running():
            scenes.update()
            app.update()

        app.join_app_proc()
