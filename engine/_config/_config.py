from .._loaders import YamlLoader
from .._special import Singleton


class ParamsContainerMeta(type):
    def __new__(mcs, values):
        def __init__(self, kwargs):
            for i in kwargs.items():
                setattr(self, *i)
            self._dct = kwargs

        def all_(self):
            return self._dct

        params = {
            "__slots__": tuple(list(values.keys()) + ['_dct']),
            "__init__": __init__,
            "all": all_
        }

        cls = super().__new__(mcs, 'ParamsContainer', (), params)
        return cls(values)


class Config(Singleton):
    def __init__(self, file):
        super().__init__()
        data = YamlLoader.load(file)
        for section_name, values in data.items():
            section = ParamsContainerMeta(values)
            setattr(self, section_name, section)
