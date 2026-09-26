from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="О боте")],
            [KeyboardButton(text="Старт"), KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
    )

    return keyboard

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт", url="https://uptime.appka.me")],
            [InlineKeyboardButton(text="Подробнее", callback_data="more_info")]
        ]
    )

    return keyboard