from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData


class UserCallbackData(CallbackData, prefix='user'):
    page: str


def user_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Получить информацию о пользователе',
        callback_data=UserCallbackData(page='get')
    )
    builder.button(
        text='Заблокировать',
        callback_data=UserCallbackData(page='block')
    )
    builder.button(
        text='Разблокировать',
        callback_data=UserCallbackData(page='activate')
    )
    builder.button(
        text='Удалить',
        callback_data=UserCallbackData(page='delete')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    builder.adjust(1, 2, 1, 1)

    return builder.as_markup()
