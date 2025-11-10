"""
Модуль для конфигурации основного цикла событий.
"""
import asyncio


current_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
