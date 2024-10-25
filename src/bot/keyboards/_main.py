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
    builder.button(
        text='Кошелек',
        callback_data=MainCallbackData(page='wallet')
    )
    builder.button(
        text='Статистика',
        callback_data=MainCallbackData(page='stats')
    )
    builder.button(
        text='Номера',
        callback_data=MainCallbackData(page='number')
    )
    builder.button(
        text='Юзернеймы',
        callback_data=MainCallbackData(page='username')
    )

    builder.adjust(1)

    return builder.as_markup()


def return_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    return builder.as_markup()


def back_kb(cb_data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='⬅️ Вернуться',
        callback_data=cb_data
    )

    return builder.as_markup()
