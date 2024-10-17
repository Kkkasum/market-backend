from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import MainCallbackData, CommissionCallbackData, SetCommissionCallbackData, commission_kb, com_kb
from src.service.admin import AdminService, CommissionType
from src.utils.formatters import format_commission

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'commission'))
async def main_commission_callback(callback: types.CallbackQuery, **_):
    m = 'Выберите комиссию'

    await callback.message.edit_text(text=m, reply_markup=commission_kb())


@router.callback_query(CommissionCallbackData.filter())
async def commission_callback(callback: types.CallbackQuery, callback_data: CommissionCallbackData):
    c = await AdminService.get_commission(callback_data.c)

    await callback.message.edit_text(text=format_commission(c), reply_markup=com_kb(callback_data.c))


@router.callback_query(SetCommissionCallbackData.filter())
async def set_commission_callback(callback: types.CallbackQuery, callback_data: SetCommissionCallbackData, state: FSMContext):
    m = 'Введите новое значение (в %, от 0 до 100)'

    await callback.message.answer(text=m)
    await state.set_state(callback_data.c)


@router.message(StateFilter(CommissionType.DEPOSIT))
async def set_deposit(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')

    except ValueError:
        m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m)

        await AdminService.set_commission(CommissionType.DEPOSIT, c / 100)
        await state.clear()


@router.message(StateFilter(CommissionType.WITHDRAWAL))
async def set_withdrawal(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')

    except ValueError:
        m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m)

        await AdminService.set_commission(CommissionType.WITHDRAWAL, c / 100)
        await state.clear()


@router.message(StateFilter(CommissionType.SWAP))
async def set_swap(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')

    except ValueError:
        m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m)

        await AdminService.set_commission(CommissionType.SWAP, c / 100)
        await state.clear()


@router.message(StateFilter(CommissionType.BUY))
async def set_buy(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')

    except ValueError:
        m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m)

        await AdminService.set_commission(CommissionType.BUY, c / 100)
        await state.clear()


@router.message(StateFilter(CommissionType.SELL))
async def set_sell(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')

    except ValueError:
        m = 'Неправильное значение (должно быть числом не больше 100 и не меньше 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m)

        await AdminService.set_commission(CommissionType.SELL, c / 100)
        await state.clear()
