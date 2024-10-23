from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData
from src.service.admin import CommissionType


class CommissionCallbackData(CallbackData, prefix='commission'):
    c: CommissionType


class SetCommissionCallbackData(CallbackData, prefix='set_commission'):
    c: CommissionType


def commission_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Вывод',
        callback_data=CommissionCallbackData(c=CommissionType.WITHDRAWAL)
    )
    builder.button(
        text='Обмен',
        callback_data=CommissionCallbackData(c=CommissionType.SWAP)
    )
    builder.button(
        text='Покупка',
        callback_data=CommissionCallbackData(c=CommissionType.BUY)
    )
    builder.button(
        text='Продажа',
        callback_data=CommissionCallbackData(c=CommissionType.SELL)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    builder.adjust(2, 1, 2, 1)

    return builder.as_markup()


def com_kb(c: CommissionType) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Установить новое значение',
        callback_data=SetCommissionCallbackData(c=c)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='commission')
    )

    return builder.as_markup()
