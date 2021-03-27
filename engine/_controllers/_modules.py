from .._special import Singleton
from .._config import Config
import importlib
import sys

__all__ = ['ModulesController']


class ModulesController(Singleton):
    __slots__ = ('_config', '_mainmd_inst', '_dependencies')

    def __init__(self):
        super().__init__()
        self._config = Config.instance()
        self._mainmd_inst = None
        self._dependencies = {}

    def _reset_dependencies(self):
        for dp in self._dependencies:
            sys.modules.pop(dp)

    def _load(self, import_func):
        state = set(sys.modules.keys())
        module = self._config.project.main_module
        self._mainmd_inst = import_func(module)
        self._dependencies = set(sys.modules) ^ state

    def load(self):
        self._load(importlib.import_module)

    def reload(self):
        self._reset_dependencies()
        self._load(importlib.reload)

    def get_class(self, classname):
        return getattr(self._mainmd_inst, classname)
