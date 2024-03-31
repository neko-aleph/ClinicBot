import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import settings
from handlers import router

TOKEN = settings.BOT_TOKEN
dp = Dispatcher()


async def main() -> None:
    bot = Bot(TOKEN)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
