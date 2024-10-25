from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData


class UserCallbackData(CallbackData, prefix='user'):
    page: str


class GetUsersCallbackData(CallbackData, prefix='get_users'):
    page: int


class UsersCallbackData(CallbackData, prefix='users'):
    user_id: int


def user_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Все пользователи', callback_data=GetUsersCallbackData(page=1))
    builder.button(
        text='Получить информацию о пользователе',
        callback_data=UserCallbackData(page='get'),
    )
    builder.button(text='Заблокировать', callback_data=UserCallbackData(page='block'))
    builder.button(
        text='Разблокировать', callback_data=UserCallbackData(page='activate')
    )
    builder.button(text='Удалить', callback_data=UserCallbackData(page='delete'))
    builder.button(text='⬅️ Вернуться', callback_data=MainCallbackData(page='main'))

    builder.adjust(1, 1, 2, 1, 1)

    return builder.as_markup()


def users_kb(users_ids: list[int], page: int, total: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.button(
            text=f'#{user_id}', callback_data=UsersCallbackData(user_id=user_id)
        )
        for user_id in users_ids
    ]

    builder.button(
        text='⬅️',
        callback_data=(
            MainCallbackData(page='user')
            if int(page) == 1
            else GetUsersCallbackData(page=str(page - 1))
        ),
    )

    builder.button(
        text=f'{page}/{total}', callback_data=GetUsersCallbackData(page=str(page))
    )

    builder.button(
        text='➡️',
        callback_data=GetUsersCallbackData(action='show', page=str(page + 1)),
    )

    builder.adjust(*[1 for _ in users_ids], 3)

    return builder.as_markup()
