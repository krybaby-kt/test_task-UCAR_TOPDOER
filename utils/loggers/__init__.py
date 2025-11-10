"""
Система логирования с цветным выводом.

Содержит настроенный logger с цветным выводом в консоль
и возможностью записи логов в файлы для отладки заказов.
"""

from typing import Any
import logging
from pathlib import Path

# Цветовая схема для различных уровней логирования
COLORS = {
    'DEBUG': '\033[94m',    # Синий
    'INFO': '\033[92m',     # Зеленый
    'WARNING': '\033[93m',  # Желтый
    'ERROR': '\033[91m',    # Красный
    'CRITICAL': '\033[91m', # Красный
    'RESET': '\033[0m',     # Сброс цвета
}


class ColoredFormatter(logging.Formatter):
    """Форматтер для цветного вывода логов в консоль."""
    def format(self, record):
        """Форматирует сообщение с добавлением цветовых кодов."""
        message = super().format(record)
        return f"{COLORS.get(record.levelname, '')}{message}{COLORS['RESET']}"


class Handler(logging.Handler):
    """Обработчик для записи логов в файлы заказов."""
    def emit(self, record):
        """
        Записывает лог сообщение в файл заказа.
        
        Извлекает path и log_filename из record и записывает
        отформатированное сообщение в соответствующий файл.
        """
        path = getattr(record, "path", None)
        log_filename = getattr(record, "log_filename", None)
        if not path or not log_filename:
            return

        with open(Path(path, f"{log_filename}.txt"), "a", encoding="utf-8") as log_file:
            log_file.write(str(self.format(record=record)) + "\n")


def _create_logger(name: str, level: int, fmt: str = None, datefmt: str = None, handler: Any = None):
    """
    Создает настроенный logger с цветным консольным выводом и файловым обработчиком.
    
    Args:
        name: Имя логгера
        level: Уровень логирования для консоли
        fmt: Формат сообщений
        datefmt: Формат даты и времени
        handler: Класс обработчика для записи в файлы
        
    Returns:
        Logger: Настроенный logger
    """
    logger = logging.getLogger(name=name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    console_formatter = ColoredFormatter(
        fmt=fmt,
        datefmt=datefmt,
    )
    
    file_formatter = logging.Formatter(
        fmt=fmt,
        datefmt=datefmt,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)
    console_handler.setFormatter(fmt=console_formatter)
    logger.addHandler(hdlr=console_handler)

    if handler:
        file_handler = handler()
        file_handler.setLevel(level=logging.DEBUG)
        file_handler.setFormatter(fmt=file_formatter)
        logger.addHandler(hdlr=file_handler)

    return logger

# Основной logger приложения с цветным выводом и записью в файлы
logger = _create_logger(
    name="logger",
    level=logging.DEBUG,
    fmt="%(asctime)s | %(levelname)s:%(name)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handler=Handler
)