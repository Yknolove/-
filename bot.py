import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from handlers import default
from aggregator import start_aggregator


async def main() -> None:
    # Создаём объект бота, передавая токен и свойства по умолчанию.
    # parse_mode через default (иначе возникнет TypeError).
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    # Настраиваем диспетчер и подключаем роутеры
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(default.router)

    # Создаём HTTP‑сессию и запускаем фоновую задачу агрегатора
    session = aiohttp.ClientSession()
    asyncio.create_task(start_aggregator(session, bot))

    # Запускаем polling
    await dp.start_polling(bot)

    # При остановке бота корректно закрываем сессию
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())
