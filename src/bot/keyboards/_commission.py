from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from src.service.admin import CommissionType


class CommissionCallbackData(CallbackData, prefix='commission'):
    c: CommissionType


class SetCommissionCallbackData(CallbackData, prefix='set_commission'):
    c: CommissionType


def commission_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Ввод',
        callback_data=CommissionCallbackData(c=CommissionType.DEPOSIT)
    )
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

    builder.adjust(2, 1, 2)

    return builder.as_markup()


def com_kb(c: CommissionType) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Установить новое значение',
        callback_data=SetCommissionCallbackData(c=c)
    )

    return builder.as_markup()
