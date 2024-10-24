from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from ._main import MainCallbackData


class WalletCallbackData(CallbackData, prefix='wallet'):
    action: str


def wallet_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text='Перевести TON',
        callback_data=WalletCallbackData(action='ton')
    )
    builder.button(
        text='Перевести NFT',
        callback_data=WalletCallbackData(action='nft')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MainCallbackData(page='main')
    )

    return builder.as_markup()
