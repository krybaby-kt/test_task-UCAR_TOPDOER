"""
Обработчик исключений для логирования и сохранения ошибок.

Предоставляет функции для детального логирования исключений с сохранением
полной информации о стеке вызовов, переменных и системной информации.
"""

from typing import Any, Dict
import traceback
import json
import uuid
from contextlib import suppress, asynccontextmanager
from traceback_with_variables import iter_exc_lines, default_format
from pathlib import Path
from configuration.paths import PATH_TO_EXCEPTIONS
from datetime import datetime
import aiofiles
import platform
from contextlib import contextmanager


default_format.max_exc_str_len = 1000000
default_format.max_value_str_len = 1000000


def get_traceback(exception: Exception, function_category: str = "", function: str = "") -> Dict[str, Any]:
    """
    Формирует детальную информацию об исключении.
    
    Args:
        exception: Исключение для анализа
        function_category: Категория функции где произошла ошибка
        function: Имя функции где произошла ошибка
        
    Returns:
        Dict: Словарь с полной информацией об исключении
    """
    result = {
        "exception_type": exception.__class__.__name__,
        "exception_message": str(exception),
        "function_category": function_category,
        "function": function,
        "standard_traceback": "\n",
        "detailed_traceback": "\n",
        "system_info": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor()
        },
        "timestamp": datetime.now().isoformat()
    }
    
    with suppress(Exception):
        result["standard_traceback"] += "".join(traceback.format_exception(type(exception), exception, exception.__traceback__, limit=None, chain=True))
    
    with suppress(Exception):
        result["detailed_traceback"] += "".join(f"{line}\n" for line in iter_exc_lines(exception))
    
    return result


def generate_exception_id() -> str:
    """
    Генерирует уникальный идентификатор для исключения.
    
    Returns:
        str: UUID4 строка в качестве уникального идентификатора
    """
    return str(uuid.uuid4())


def create_exception_filename(exception_id: str, function_category: str, function: str) -> str:
    """
    Создает имя файла для сохранения информации об исключении.
    
    Args:
        exception_id: Уникальный идентификатор исключения
        function_category: Категория функции
        function: Название функции
        
    Returns:
        str: Имя файла в формате '[ID дата] категория функция.json'
    """
    current_date = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
    return f"[{exception_id} {current_date}] {function_category} {function}.json"


def handle_sync(function_category: str, function: str, exception: Any) -> str:
    """
    Синхронно обрабатывает и сохраняет исключение.
    
    Args:
        function_category: Категория функции где произошла ошибка
        function: Имя функции где произошла ошибка
        exception: Исключение для обработки
        
    Returns:
        str: Имя файла с сохраненной информацией об исключении
    """
    exception_data = get_traceback(exception, function_category, function)
    exception_id = generate_exception_id()
    filename = create_exception_filename(exception_id, function_category, function)
    file_path = Path(PATH_TO_EXCEPTIONS, filename)
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(exception_data, file, ensure_ascii=False, indent=2)
        
    return filename


async def handle_async(function_category: str, function: str, exception: Any) -> str:
    """
    Асинхронно обрабатывает и сохраняет исключение.
    
    Args:
        function_category: Категория функции где произошла ошибка
        function: Имя функции где произошла ошибка
        exception: Исключение для обработки
        
    Returns:
        str: Имя файла с сохраненной информацией об исключении
    """
    exception_data = get_traceback(exception=exception, function_category=function_category, function=function)
    exception_id = generate_exception_id()
    filename = create_exception_filename(exception_id=exception_id, function_category=function_category, function=function)
    file_path = Path(PATH_TO_EXCEPTIONS, filename)
    
    async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
        await file.write(json.dumps(exception_data, ensure_ascii=False, indent=2))
    
    return filename


@asynccontextmanager
async def exception_context_async(function_category: str, function: str):
    try:
        yield
    except Exception as ex_:
        await handle_async(function_category=function_category, function=function, exception=ex_)
        raise


@contextmanager
def exception_context_sync(function_category: str, function: str):
    try:
        yield
    except Exception as ex_:
        handle_sync(function_category=function_category, function=function, exception=ex_)
        raise
        