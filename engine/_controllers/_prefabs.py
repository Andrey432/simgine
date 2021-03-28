from .._types.objects import Prefab
from .._special import Singleton
from .._loaders import YamlLoader
from ._modules import ModulesController
from ._config import Config

__all__ = ['PrefabsController']


class PrefabsController(Singleton):
    __slots__ = ('_config', '_prefabs', '_modules')

    def __init__(self):
        super().__init__()
        self._config = Config.instance()
        self._modules = ModulesController.instance()
        self._prefabs = {}

    def init(self):
        file = self._config.get('project/gameobjects')
        prefabs = YamlLoader.load(file)["prefabs"]
        main_module = self._modules

        for name, data in prefabs.items():
            class_ = main_module.get_class(data['class'])
            prefab = Prefab(name, class_, data.get('params', {}))
            self._prefabs[name] = prefab

    def create(self, prefabname: str, kwargs: dict):
        prefab = self._prefabs.get(prefabname)
        if prefab is not None:
            return prefab.create(kwargs)
