from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


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
