from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from src.bot.keyboards import MainCallbackData, return_main_kb
from src.service.number import NumberService

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'number'))
async def main_number_callback(callback: types.CallbackQuery, state: FSMContext, **_):
    await callback.message.delete()
    await callback.message.answer(text='Введите номер')

    await state.set_state('number')


@router.message(StateFilter('number'))
async def number(message: types.Message, state: FSMContext):
    number = message.text.replace('+', '').replace(' ', '')

    address = await NumberService.get_address_by_number(number)
    if not address:
        await message.answer(text=f'Номер {number} не найден', reply_markup=return_main_kb())
    else:
        await message.answer(text=f'Адрес NFT: <code>{address}</code>', reply_markup=return_main_kb())

    await state.clear()
