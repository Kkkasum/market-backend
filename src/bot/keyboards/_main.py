from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


class MainCallbackData(CallbackData, prefix='main'):
    page: str


def main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Комиссии',
        callback_data=MainCallbackData(page='fee')
    )
    builder.button(
        text='Пользователи',
        callback_data=MainCallbackData(page='user')
    )

    builder.adjust(1)

    return builder.as_markup()


def back_kb(cb_data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='⬅️ Вернуться',
        callback_data=cb_data
    )

    return builder.as_markup()
