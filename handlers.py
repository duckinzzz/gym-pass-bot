import asyncio

from aiogram import F, Router, types
from aiogram.filters import CommandStart

import keyboards as kb
from config import ADMIN_ID, START_MESSAGE_TEXT
from keyboards import REFRESH_QR_CALLBACK
from utils import get_qr, send_error

start_router = Router(name="start_router")
start_router.message.filter(F.from_user.id == ADMIN_ID)
start_router.callback_query.filter(F.from_user.id == ADMIN_ID)


@start_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    try:
        await message.answer(
            START_MESSAGE_TEXT,
            reply_markup=await kb.refresh_kb(),
        )
    except Exception as error:
        await send_error(message.bot, message.chat.id, error)


@start_router.callback_query(F.data == REFRESH_QR_CALLBACK)
async def refresh_qr(callback: types.CallbackQuery) -> None:
    await callback.answer()

    if not callback.message:
        return
    loading_msg = await callback.message.answer('Загрузка...')
    photo, valid_time, qr_path = await get_qr()
    try:
        await loading_msg.delete()
        qr_message = await callback.message.answer_photo(
            photo=photo,
        )
    finally:
        await asyncio.to_thread(qr_path.unlink, missing_ok=True)

    await asyncio.sleep(valid_time)
    await qr_message.delete()
