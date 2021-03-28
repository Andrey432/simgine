from pathlib import Path

__all__ = ['BASE_DIR', 'CONFIG_FILE']


BASE_DIR = Path(__file__).parents[1]
CONFIG_FILE = BASE_DIR / 'data/config.yaml'
DEBUG = True
