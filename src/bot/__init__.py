from aiogram import Dispatcher

from src.bot.handlers import (
    main_router, user_router, const_router, wallet_router, stats_router, number_router, username_router
)


def include_routers(dp: Dispatcher):
    dp.include_routers(
        main_router,
        user_router,
        const_router,
        wallet_router,
        stats_router,
        number_router,
        username_router
    )
