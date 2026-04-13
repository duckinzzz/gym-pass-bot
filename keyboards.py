from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import REFRESH_BUTTON_TEXT

REFRESH_QR_CALLBACK = "refresh_qr"


async def refresh_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=REFRESH_BUTTON_TEXT, style='success', callback_data=REFRESH_QR_CALLBACK)],
        ]
    )
