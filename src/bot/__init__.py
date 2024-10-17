from aiogram import Dispatcher

from src.bot.handlers import main_router, user_router, commission_router


def include_routers(dp: Dispatcher):
    dp.include_routers(
        main_router,
        user_router,
        commission_router
    )
    