import yaml
from pathlib import Path


def YAML_format(file):
    with open(Path(file), 'r', encoding='utf-8') as file_d:
        return yaml.safe_load(file_d)
