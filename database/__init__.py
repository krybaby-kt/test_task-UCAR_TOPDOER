"""
Модуль для инициализации моделей базы данных.
"""
from database.base import engine, Base


async def init_models():
    """
    Инициализация моделей базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
