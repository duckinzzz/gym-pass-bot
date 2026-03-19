from aiogram import Router, types, F
from aiogram.filters import CommandStart

import keyboards as kb
from core import logger

start_router = Router()


def get_user_name(user: types.User):
    if user.username:
        return f"@{user.username}"
    else:
        return f"{user.first_name or user.id}"


@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = get_user_name(message.from_user)
    uid = message.from_user.id

    welcome_text = (
        f"aiogram template with echo-bot"
    )

    await message.answer(
        welcome_text,
        reply_markup=kb.main_kb(uid)
    )

    logger.info(f"User {user_name} ({uid}) started the bot")


@start_router.callback_query(F.data.split(':')[2] == 'default_button')
async def process_button(callback: types.CallbackQuery):
    await callback.answer('You pressed the button')


@start_router.message()
async def universal_handler(message: types.Message):
    user_name = get_user_name(message.from_user)
    content_type = str(message.content_type).split('.')[1]
    text = message.text or message.caption
    logger.info(f"\nuserID: {message.from_user.id}\nusername: {user_name}\ncontent_type: {content_type}\ntext: {text}")
    await message.answer(f"userID: {message.from_user.id}\n"
                         f"username: {user_name}\n"
                         f"content_type: {content_type}\n"
                         f"text: {text}")
