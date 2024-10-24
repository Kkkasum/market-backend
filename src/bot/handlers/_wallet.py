from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.common import config
from src.bot.keyboards import MainCallbackData, WalletCallbackData, wallet_kb, return_main_kb
from src.service.withdrawal import WithdrawalService
from src.utils.formatters import format_wallet
from src.utils import messages as msg

router = Router()


@router.callback_query(MainCallbackData.filter(F.page == 'wallet'))
async def main_wallet_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()
    await callback.message.answer(text=format_wallet(config.TON_WALLET_ADDRESS), reply_markup=wallet_kb())


@router.callback_query(WalletCallbackData.filter(F.action == 'ton'))
async def wallet_ton_callback(callback: types.CallbackQuery, state: FSMContext, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.wallet_ton)

    await state.set_state('ton')


@router.callback_query(WalletCallbackData.filter(F.action == 'nft'))
async def wallet_nft_callback(callback: types.CallbackQuery, state: FSMContext, **_):
    await callback.message.delete()
    await callback.message.answer(text=msg.wallet_nft)

    await state.set_state('nft')


@router.message(StateFilter('ton'))
async def transfer_ton(message: types.Message, state: FSMContext):
    try:
        destination, amount = message.text.split(':')
    except Exception:
        m = 'Неправильный формат данных'

        await message.answer(text=m, reply_markup=return_main_kb())
        return

    await WithdrawalService.withdraw_ton(user_id=1, destination=destination, amount=amount)

    await state.clear()


@router.message(StateFilter('nft'))
async def transfer_nft(message: types.Message, state: FSMContext):
    try:
        destination, nft_address = message.text.split(':')
    except Exception:
        m = 'Неправильный формат данных'

        await message.answer(text=m, reply_markup=return_main_kb())
        return

    await WithdrawalService.withdraw_nft(user_id=1, destination=destination, nft_address=nft_address)

    await state.clear()
