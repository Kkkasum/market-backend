from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import (
    MainCallbackData, FeeCallbackData, SetFeeCallbackData, back_kb, fee_kb, com_kb
)
from src.service.admin import AdminService, FeeType
from src.utils.formatters import format_fee

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'fee'))
async def main_fee_callback(callback: types.CallbackQuery, **_):
    m = 'Выберите комиссию'

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=fee_kb())


@router.callback_query(FeeCallbackData.filter())
async def fee_callback(callback: types.CallbackQuery, callback_data: FeeCallbackData):
    c = await AdminService.get_fee(callback_data.c)

    await callback.message.delete()

    if callback_data.c == FeeType.WITHDRAWAL_TRON:
        await callback.message.answer(text=format_fee(c, extra=' USDT'), reply_markup=com_kb(callback_data.c))
    elif callback_data.c == FeeType.WITHDRAWAL_TON:
        await callback.message.answer(text=format_fee(c, extra=' TON'), reply_markup=com_kb(callback_data.c))
    else:
        await callback.message.answer(text=format_fee(c, extra='%'), reply_markup=com_kb(callback_data.c))


@router.callback_query(SetFeeCallbackData.filter())
async def set_fee_callback(
    callback: types.CallbackQuery, callback_data: SetFeeCallbackData, state: FSMContext
):
    m = 'Введите новое значение'

    await callback.message.answer(text=m)
    await state.set_state(callback_data.c)


@router.message(StateFilter(FeeType.WITHDRAWAL_TRON))
async def set_withdrawal_tron(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c < 0:
            m = 'Неправильное значение (должно быть числом > 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом > 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение')
        return
    else:
        m = 'Новая комиссия установлена'

        await message.answer(text=m, reply_markup=back_kb(MainCallbackData(page='fee')))

        await AdminService.set_fee(FeeType.WITHDRAWAL_TRON, c)
        await state.clear()


@router.message(StateFilter(FeeType.WITHDRAWAL_TON))
async def set_withdrawal_ton(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c < 0:
            m = 'Неправильное значение (должно быть числом > 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом > 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение')
        return
    else:
        m = 'Новая комиссия установлена'

        await message.answer(text=m, reply_markup=back_kb(MainCallbackData(page='fee')))

        await AdminService.set_fee(FeeType.WITHDRAWAL_TON, c)
        await state.clear()


@router.message(StateFilter(FeeType.SWAP))
async def set_swap(message: types.Message, state: FSMContext):
    try:
        c = int(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом < 100 и > 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом < 100 и > 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлена'

        await message.answer(text=m, reply_markup=back_kb(MainCallbackData(page='fee')))

        await AdminService.set_fee(FeeType.SWAP, c)
        await state.clear()


@router.message(StateFilter(FeeType.BUY))
async def set_buy(message: types.Message, state: FSMContext):
    try:
        c = int(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом < 100 и > 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом < 100 и > 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m, reply_markup=back_kb(MainCallbackData(page='fee')))

        await AdminService.set_fee(FeeType.BUY, c)
        await state.clear()


@router.message(StateFilter(FeeType.SELL))
async def set_sell(message: types.Message, state: FSMContext):
    try:
        c = int(message.text)
        if c > 100 or c < 0:
            m = 'Неправильное значение (должно быть числом < 100 и > 0)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение (в %)')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом < 100 и > 0)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение (в %)')
        return
    else:
        m = 'Новая комиссия установлено'

        await message.answer(text=m, reply_markup=back_kb(MainCallbackData(page='fee')))

        await AdminService.set_fee(FeeType.SELL, c)
        await state.clear()
