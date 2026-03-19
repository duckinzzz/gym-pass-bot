import asyncio

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart

import keyboards as kb
from config import ADMIN_ID, QR_EXPIRED_TEXT, START_MESSAGE_TEXT
from keyboards import REFRESH_QR_CALLBACK
from utils import get_qr, send_error

start_router = Router(name="start_router")
start_router.message.filter(F.from_user.id == ADMIN_ID)
start_router.callback_query.filter(F.from_user.id == ADMIN_ID)

expire_tasks: dict[int, asyncio.Task[None]] = {}


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
    chat_id = callback.message.chat.id if callback.message else callback.from_user.id

    try:
        await callback.answer()

        if not callback.message:
            return

        task = expire_tasks.pop(chat_id, None)
        if task:
            task.cancel()

        try:
            await callback.message.delete()
        except TelegramBadRequest as error:
            if "message to delete not found" not in str(error).lower():
                raise

        photo, valid_time, qr_path = await get_qr()
        try:
            qr_message = await callback.message.answer_photo(
                photo=photo,
                reply_markup=await kb.refresh_kb(),
            )
        finally:
            await asyncio.to_thread(qr_path.unlink, missing_ok=True)

        async def expire() -> None:
            try:
                await asyncio.sleep(valid_time)
                await callback.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=qr_message.message_id,
                    caption=QR_EXPIRED_TEXT,
                    reply_markup=await kb.refresh_kb(),
                )
                expire_tasks.pop(chat_id, None)
            except asyncio.CancelledError:
                return
            except TelegramBadRequest as error:
                text = str(error).lower()
                if "message to edit not found" in text or "message is not modified" in text:
                    return
                await send_error(callback.bot, chat_id, error)
            except Exception as error:
                await send_error(callback.bot, chat_id, error)

        expire_tasks[chat_id] = asyncio.create_task(expire())
    except Exception as error:
        await send_error(callback.bot, chat_id, error)
