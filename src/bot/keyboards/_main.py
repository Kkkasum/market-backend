from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._commission import CommissionCallbackData
from ._user import UserCallbackData


class MainCallbackData(CallbackData, prefix='main'):
    page: str


def main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Комиссии',
        callback_data=MainCallbackData(page='commission')
    )
    builder.button(
        text='Пользователи',
        callback_data=MainCallbackData(page='user')
    )

    builder.adjust(1)

    return builder.as_markup()


def back_kb(cb_data: MainCallbackData | CommissionCallbackData | UserCallbackData) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='⬅️ Вернуться',
        callback_data=cb_data
    )

    return builder.as_markup()
