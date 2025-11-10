"""
Модуль для конфигурации env файла.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


__env_file__: str = ".env" # Название env файла


class Settings(BaseSettings):
    """
    Класс для конфигурации env файла.
    """
    BACKEND_HOST: str
    BACKEND_PORT: int

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        """
        URL для подключения к базе данных asyncpg.
        """
        return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    @property
    def DATABASE_URL_psycopg(self):
        """
        URL для подключения к базе данных psycopg.
        """
        return f"postgresql+psycopg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    model_config = SettingsConfigDict(env_file=__env_file__) # Конфигурация env файла


settings = Settings() # Экземпляр класса Settings


if __name__ == "__main__":
    """
    Основная функция для тестирования конфигурации.
    """
    print(settings.DATABASE_URL_asyncpg)
    print(settings.DATABASE_URL_psycopg)