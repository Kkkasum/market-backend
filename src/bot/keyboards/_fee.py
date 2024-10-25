from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData
from src.service.admin import FeeType


class FeeCallbackData(CallbackData, prefix='fee'):
    c: FeeType


class SetFeeCallbackData(CallbackData, prefix='set_fee'):
    c: FeeType


def fee_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Вывод TRON',
        callback_data=FeeCallbackData(c=FeeType.WITHDRAWAL_TRON)
    )
    builder.button(
        text='Вывод TON',
        callback_data=FeeCallbackData(c=FeeType.WITHDRAWAL_TON)
    )
    builder.button(
        text='Обмен',
        callback_data=FeeCallbackData(c=FeeType.SWAP)
    )
    builder.button(
        text='Покупка',
        callback_data=FeeCallbackData(c=FeeType.BUY)
    )
    builder.button(
        text='Продажа',
        callback_data=FeeCallbackData(c=FeeType.SELL)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    builder.adjust(2, 1, 2, 1)

    return builder.as_markup()


def com_kb(c: FeeType) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Установить новое значение',
        callback_data=SetFeeCallbackData(c=c)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='fee')
    )

    builder.adjust(1, 1)

    return builder.as_markup()
