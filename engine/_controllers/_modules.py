import importlib
import sys
from .._special import Singleton
from ._config import Config

__all__ = ['ModulesController']


class ModulesController(Singleton):
    __slots__ = ('_config', '_modules', '_dependencies')

    def __init__(self):
        super().__init__()
        self._config = Config.instance()
        self._modules = {}
        self._dependencies = {}

    def _reset_dependencies(self):
        for dp in self._dependencies:
            sys.modules.pop(dp)

    def _load(self, importer):
        state = set(sys.modules.keys())
        md_list = self._config.get('includes')
        self._modules = {i: importer(i) for i in md_list}
        self._dependencies = set(sys.modules) ^ state

    def init(self):
        self._load(importlib.import_module)

    def reload(self):
        self._reset_dependencies()
        self._load(importlib.reload)

    def get_attr(self, name: str):
        for md in self._modules.values():
            if hasattr(md, name):
                return getattr(md, name)
