import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot import include_routers
from src.common import config


async def main():
    bot = Bot(
        token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    include_routers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
