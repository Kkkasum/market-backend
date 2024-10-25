from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData
from src.service.admin import Const


class ConstCallbackData(CallbackData, prefix='const'):
    c: Const


class SetConstCallbackData(CallbackData, prefix='set_const'):
    c: Const


def const_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Процент автовыкупа',
        callback_data=ConstCallbackData(c=Const.INSTANT_SELL_PERC)
    )
    builder.button(
        text='Максимальная цена автовыкупа',
        callback_data=ConstCallbackData(c=Const.MAX_INSTANT_SELL)
    )
    builder.button(
        text='Вывод TRON',
        callback_data=ConstCallbackData(c=Const.FEE_WITHDRAWAL_TRON)
    )
    builder.button(
        text='Вывод TON',
        callback_data=ConstCallbackData(c=Const.FEE_WITHDRAWAL_TON)
    )
    builder.button(
        text='Обмен',
        callback_data=ConstCallbackData(c=Const.FEE_SWAP)
    )
    builder.button(
        text='Покупка',
        callback_data=ConstCallbackData(c=Const.FEE_BUY)
    )
    builder.button(
        text='Продажа',
        callback_data=ConstCallbackData(c=Const.FEE_SELL)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    builder.adjust(2, 2, 1, 2, 1)

    return builder.as_markup()


def com_kb(c: Const) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Установить новое значение',
        callback_data=SetConstCallbackData(c=c)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='const')
    )

    builder.adjust(1, 1)

    return builder.as_markup()
