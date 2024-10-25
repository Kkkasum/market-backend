from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from src.bot.keyboards import MainCallbackData, return_main_kb
from src.service.username import UsernameService

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'username'))
async def main_username_callback(callback: types.CallbackQuery, state: FSMContext, **_):
    await callback.message.delete()
    await callback.message.answer(text='Введите юзернейм')

    await state.set_state('username')


@router.message(StateFilter('username'))
async def get_username(message: types.Message, state: FSMContext):
    username = message.text.replace('+', '').replace(' ', '')

    address = await UsernameService.get_address_by_username(username)
    if not address:
        await message.answer(text=f'Юзернейм {username} не найден', reply_markup=return_main_kb())
    else:
        await message.answer(text=f'Адрес NFT: <code>{address}</code>', reply_markup=return_main_kb())

    await state.clear()
