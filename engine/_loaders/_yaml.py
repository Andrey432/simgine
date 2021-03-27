import yaml
from typing import Callable, Any, Union
from pathlib import Path

__all__ = ['YamlLoader']


def dumper_decorator(func, tag):
    def wrapper(dumper, value):
        return dumper.represent_scalar(tag, func(value))
    return wrapper


class YamlLoader:
    @staticmethod
    def add_loader(tag: str, loader: Callable[[yaml.SafeLoader, yaml.Node], Any]):
        yaml.SafeLoader.add_constructor(f'!{tag}', loader)

    @staticmethod
    def add_dumper(tag: str, type_: type, func: Callable[[Any], Any]):
        yaml.SafeDumper.add_multi_representer(type_, dumper_decorator(func, f'!{tag}'))

    @staticmethod
    def load(file: Union[str, Path], encoding='utf-8', default=None):
        try:
            with open(Path(file), 'r', encoding=encoding) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            if default is None:
                raise
            return default

    @staticmethod
    def save(file: Union[str, Path], data: Any, mode='w', encoding='utf-8', default=None):
        try:
            with open(Path(file), mode, encoding=encoding) as f:
                yaml.safe_dump(data, f)
        except FileNotFoundError:
            if default is None:
                raise
            return default
