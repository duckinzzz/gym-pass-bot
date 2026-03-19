from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def _mk(buttons):
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_kb(uid: int):
    return _mk([
        [InlineKeyboardButton(text="Button", callback_data=f"user:{uid}:default_button"), ],
    ])
