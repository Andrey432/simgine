from .._scene import Scene
from .._loaders import YAML_format
from .._special import Singleton
from .._config import Config

__all__ = ['ScenesController']


class ScenesController(Singleton):
    def __init__(self):
        super().__init__()
        self._config = Config.instance()
        self._scenes = {}
        self._current_scene = None

    def init(self):
        data = YAML_format(self._config.project.gameobjects)['scenes']
        for scene_name, scene_data in data.items():
            self._scenes[scene_name] = Scene(scene_data)
        self._current_scene = self._scenes[self._config.project.defaultscene]

    def change_scene(self, scene_name):
        self._current_scene = self._scenes[scene_name]

    def current_scene(self):
        return self._current_scene
    
    def update(self):
        self._current_scene.update()
