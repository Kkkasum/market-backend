from aiogram import Router, types, F
from aiogram.filters import CommandStart

from src.common import config
from src.bot.keyboards import MainCallbackData, main_kb

router = Router()


@router.message(CommandStart(), F.from_user.id == config.ADMIN_ID)
async def start(message: types.Message):
    m = 'Выберите раздел'

    await message.answer(text=m, reply_markup=main_kb())


@router.callback_query(MainCallbackData.filter(F.page == 'main'))
async def start_callback(callback: types.CallbackQuery, callback_data: MainCallbackData):
    m = 'Выберите раздел'

    await callback.message.answer(text=m, reply_markup=main_kb())
