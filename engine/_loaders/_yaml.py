import yaml
from typing import Callable, Any, Union
from pathlib import Path

__all__ = ['YamlLoader']


class YamlLoader:
    @staticmethod
    def add_handler(tag: str, handler: Callable[[yaml.SafeLoader, yaml.Node], Any]):
        yaml.SafeLoader.add_constructor(f'!{tag}', handler)

    @staticmethod
    def load(file: Union[str, Path], default: Any = None) -> Union[list, dict, None]:
        try:
            with open(Path(file), 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            if default is None:
                raise
            return default

    @staticmethod
    def save():
        pass
