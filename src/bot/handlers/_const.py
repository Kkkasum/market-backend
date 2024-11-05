from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import (
    MainCallbackData,
    ConstCallbackData,
    SetConstCallbackData,
    back_kb,
    const_kb,
    com_kb,
)
from src.service.admin import AdminService, Const
from src.utils.formatters import format_const

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'const'))
async def main_const_callback(callback: types.CallbackQuery, **_):
    m = 'Выберите комиссию'

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=const_kb())


@router.callback_query(ConstCallbackData.filter())
async def const_callback(
    callback: types.CallbackQuery, callback_data: ConstCallbackData
):
    c = await AdminService.get_constant(callback_data.c)

    await callback.message.delete()

    if callback_data.c == Const.FEE_WITHDRAWAL_TRON:
        await callback.message.answer(
            text=format_const(c, extra=' USDT'), reply_markup=com_kb(callback_data.c)
        )
    elif (
        callback_data.c == Const.FEE_WITHDRAWAL_TON
        or callback_data.c == Const.MAX_INSTANT_SELL
    ):
        await callback.message.answer(
            text=format_const(c, extra=' TON'), reply_markup=com_kb(callback_data.c)
        )
    else:
        await callback.message.answer(
            text=format_const(c, extra='%'), reply_markup=com_kb(callback_data.c)
        )


@router.callback_query(SetConstCallbackData.filter())
async def set_constant_callback(
    callback: types.CallbackQuery,
    callback_data: SetConstCallbackData,
    state: FSMContext,
):
    m = 'Введите новое значение'

    await callback.message.answer(text=m)
    await state.set_state(callback_data.c)


@router.message(StateFilter(Const.INSTANT_SELL_PERC))
async def set_instant_sell_perc(message: types.Message, state: FSMContext):
    try:
        c = float(message.text)
        if c < 0:
            m = 'Неправильное значение (должно быть числом > 0 и < 100, %)'

            await message.answer(text=m)
            await message.answer(text='Введите новое значение')
            return
    except ValueError:
        m = 'Неправильное значение (должно быть числом > 0 и < 100, %)'

        await message.answer(text=m)
        await message.answer(text='Введите новое значение')
        return
    else:
        await AdminService.set_constant(Const.INSTANT_SELL_PERC, c)

        await message.answer(
            text='Новое значение установлено',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.MAX_INSTANT_SELL))
async def set_max_instant_sell(message: types.Message, state: FSMContext):
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
        await AdminService.set_constant(Const.MAX_INSTANT_SELL, c)

        await message.answer(
            text='Новое значение установлено',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_RUB_DEPOSIT))
async def set_rub_deposit(message: types.Message, state: FSMContext):
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
        await AdminService.set_constant(Const.FEE_RUB_DEPOSIT, c)

        await message.answer(
            text='Новая комиссия установлено',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_WITHDRAWAL_TRON))
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
        await AdminService.set_constant(Const.FEE_WITHDRAWAL_TRON, c)

        await message.answer(
            text='Новая комиссия установлена',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_WITHDRAWAL_TON))
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
        await AdminService.set_constant(Const.FEE_WITHDRAWAL_TON, c)

        await message.answer(
            text='Новая комиссия установлена',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_SWAP))
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
        await AdminService.set_constant(Const.FEE_SWAP, c)

        await message.answer(
            text='Новая комиссия установлена',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_BUY))
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
        await AdminService.set_constant(Const.FEE_BUY, c)

        await message.answer(
            text='Новая комиссия установлено',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()


@router.message(StateFilter(Const.FEE_SELL))
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
        await AdminService.set_constant(Const.FEE_SELL, c)

        await message.answer(
            text='Новая комиссия установлено',
            reply_markup=back_kb(MainCallbackData(page='const')),
        )

        await state.clear()
