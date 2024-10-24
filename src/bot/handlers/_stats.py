from datetime import datetime, timedelta

from aiogram import Router, types, F

from src.bot.keyboards import MainCallbackData, return_main_kb
from src.service.history import HistoryService
from src.utils.formatters import format_stats

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'stats'))
async def main_stats_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()

    current_time = datetime.now()

    withdrawals, deposits, swaps = await HistoryService.get_stats(
        start_time=current_time - timedelta(days=1), end_time=current_time
    )
    await callback.message.answer(
        text=format_stats(
            period='1 день',
            withdrawals=withdrawals,
            deposits=deposits,
            swaps=swaps
        )
    )

    withdrawals, deposits, swaps = await HistoryService.get_stats(
        start_time=current_time - timedelta(weeks=1), end_time=current_time
    )
    await callback.message.answer(
        text=format_stats(
            period='7 дней',
            withdrawals=withdrawals,
            deposits=deposits,
            swaps=swaps
        )
    )

    withdrawals, deposits, swaps = await HistoryService.get_stats(
        start_time=current_time - timedelta(days=30), end_time=current_time
    )
    await callback.message.answer(
        text=format_stats(
            period='30 дней',
            withdrawals=withdrawals,
            deposits=deposits,
            swaps=swaps
        )
    )

    withdrawals, deposits, swaps = await HistoryService.get_stats()
    await callback.message.answer(
        text=format_stats(
            period='все время',
            withdrawals=withdrawals,
            deposits=deposits,
            swaps=swaps
        ),
        reply_markup=return_main_kb()
    )
