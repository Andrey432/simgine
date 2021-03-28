from .._loaders import YamlLoader
from .._special import Singleton
from .._constants.settings import CONFIG_FILE


class Config(Singleton):
    def __init__(self):
        super().__init__()
        self._data = YamlLoader.load(CONFIG_FILE)

    def get(self, value: str):
        if '/' in value:
            section, var = value.split('/')
            return self._data[section][var]
        return self._data[value]
