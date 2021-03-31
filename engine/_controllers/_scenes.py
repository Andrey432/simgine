from ._config import Config
from .._scene import Scene
from .._loaders import YamlLoader
from .._special import Singleton

__all__ = ['ScenesController']


class ScenesController(Singleton):
    def __init__(self):
        super().__init__()
        self._config = Config.instance()
        self._scenes = {}
        self._current_scene = None

    def init(self):
        file = self._config.get('project/gameobjects')
        data = YamlLoader.load(file)['scenes']
        for scene_name, scene_data in data.items():
            self._scenes[scene_name] = Scene(scene_data)
        default = self._config.get('project/defaultscene')
        self._current_scene = self._scenes[default]

    def change_scene(self, scene_name):
        self._current_scene = self._scenes[scene_name]

    def current_scene(self):
        return self._current_scene

    def update(self):
        self._current_scene.update()
