from .._loaders import YamlLoader
from .._special import Singleton
from .._constants.settings import CONFIG_FILE


class Config(Singleton):
    def __init__(self):
        super().__init__()
        self._data = YamlLoader.load(CONFIG_FILE)

    def init(self):
        additional_cnf = self._data['project']['additional_cnf']
        data = YamlLoader.load(additional_cnf, default={})

        for k, v in data.items():
            if k in self._data and isinstance(v, dict):
                self._data[k].update(v)
            else:
                self._data[k] = v

    def get(self, value: str):
        if '/' in value:
            section, var = value.split('/')
            return self._data[section][var]
        return self._data[value]
