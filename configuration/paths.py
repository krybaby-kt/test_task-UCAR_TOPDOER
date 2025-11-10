"""
Модуль для конфигурации путей.
"""
from pathlib import Path


PATH_TO_ASSETS = Path("assets")
PATH_TO_ASSETS.mkdir(parents=True, exist_ok=True)

PATH_TO_EXCEPTIONS = Path(PATH_TO_ASSETS, "exceptions")
PATH_TO_EXCEPTIONS.mkdir(parents=True, exist_ok=True)
