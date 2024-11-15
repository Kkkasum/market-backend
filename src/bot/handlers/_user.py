from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import (
    MainCallbackData,
    UserCallbackData,
    GetUsersCallbackData,
    UsersCallbackData,
    user_kb,
    users_kb,
    return_main_kb,
)
from src.service.admin import AdminService
from src.service.user import UserService
from src.utils.formatters import format_user

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'user'))
async def main_user_callback(callback: types.CallbackQuery, **_):
    m = 'Выберите действие'

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=user_kb())


@router.callback_query(GetUsersCallbackData.filter())
async def get_users_callback(
    callback: types.CallbackQuery, callback_data: GetUsersCallbackData
):
    users_ids = await UserService.get_users_ids()
    if not users_ids:
        await callback.message.edit_text(text='Пользователи не найдены')
        return

    total = (
        len(users_ids) // 5
        if len(users_ids) // 5 == len(users_ids) / 5
        else len(users_ids) // 5 + 1
    )

    start = int(callback_data.page - 1) * 5
    end = start + 5

    if int(callback_data.page) > total:
        return

    await callback.message.edit_text(
        text='Пользователи',
        reply_markup=users_kb(
            users_ids[start:end], page=int(callback_data.page), total=total
        ),
    )


@router.callback_query(UsersCallbackData.filter())
async def get_user_callback(
    callback: types.CallbackQuery, callback_data: UsersCallbackData
):
    user = await UserService.get_user(user_id=callback_data.user_id)

    await callback.message.delete()
    await callback.message.answer(
        text=format_user(callback_data.user_id, user), reply_markup=return_main_kb()
    )


@router.callback_query(UserCallbackData.filter())
async def user_callback(
    callback: types.CallbackQuery, callback_data: UserCallbackData, state: FSMContext
):
    m = 'Введите ID пользователя'

    await callback.message.answer(text=m)
    await state.set_state(callback_data.page)


@router.message(StateFilter('get'))
async def get_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        m = 'Введите число'

        await message.answer(text=m)
    else:
        user = await UserService.get_user(user_id)
        if not user:
            m = f'Пользователь {user_id} не найден'

            await message.answer(text=m)
            await state.clear()
            return

        await message.answer(text=format_user(user_id, user))
        await state.clear()


@router.message(StateFilter('block'))
async def block_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        m = 'Введите число'

        await message.answer(text=m)
    else:
        user = await UserService.get_user(user_id)
        if not user:
            m = f'Пользователь {user_id} не найден'

            await message.answer(text=m)
            await state.clear()
            return

        m = f'Пользователь {user_id} заблокирован'

        await message.answer(text=m)

        await AdminService.block_user(user_id)
        await state.clear()


@router.message(StateFilter('activate'))
async def activate_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        m = 'Введите число'

        await message.answer(text=m)
    else:
        user = await UserService.get_user(user_id)
        if not user:
            m = f'Пользователь {user_id} не найден'

            await message.answer(text=m)
            await state.clear()
            return

        m = f'Пользователь {user_id} активирован'

        await message.answer(text=m)

        await AdminService.activate_user(user_id)
        await state.clear()


@router.message(StateFilter('delete'))
async def block_user(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        m = 'Введите число'

        await message.answer(text=m)
    else:
        user = await UserService.get_user(user_id)
        if not user:
            m = f'Пользователь {user_id} не найден'

            await message.answer(text=m)
            await state.clear()
            return

        m = f'Пользователь {user_id} удален'

        await message.answer(text=m)

        await AdminService.delete_user(user_id)
        await state.clear()
