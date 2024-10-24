from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.common import config
from src.bot.keyboards import MainCallbackData, main_kb

router = Router()


@router.message(CommandStart(), F.from_user.id == config.ADMIN_ID)
async def start(message: types.Message):
    m = 'Выберите раздел'

    await message.answer(text=m, reply_markup=main_kb())


@router.callback_query(MainCallbackData.filter(F.page == 'main'))
async def start_callback(callback: types.CallbackQuery, state: FSMContext, **_):
    m = 'Выберите раздел'

    await state.clear()

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=main_kb())
