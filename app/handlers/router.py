import html
import logging

from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.settings.config import AppSettings
from app.settings.access import AccessMiddleware
from app.handlers.keyboard import (
    get_main_reply_keyboard,
    get_main_inline_keyboard,
)

module_logger = logging.getLogger(__name__)

def create_router(settings: AppSettings) -> Router:
    """Create handlers that share the validated application settings."""

    router = Router(name=__name__)

    access = AccessMiddleware(settings)
    for observer in (router.message, router.callback_query):
        observer.outer_middleware(access)

    @router.message(CommandStart())
    @router.message(F.text.lower() == "старт")
    async def handle_start(message: Message) -> None:
        user = message.from_user
        if user is None:
            return

        display_name = html.escape(user.first_name)
        await message.answer(
            f"Привет, {display_name}!",
            reply_markup=get_main_inline_keyboard()
        )

    @router.message(Command('help'))
    @router.message(F.text.lower() == "помощь")
    async def helper(message: Message):
        await message.answer(f"# Команды:\n\n"
                             f"/start - запустить бота\n"
                             f"/help - помощь\n"
                             f"/about - о боте\n\n"
                             f"*Other commands coming soon!* 😉",
                             parse_mode='Markdown')


    @router.callback_query(F.data == "more_info")
    async def process_more_info(callback: CallbackQuery) -> None:
        await callback.answer()
        if isinstance(callback.message, Message):
            await callback.message.answer("Заглушка")


    @router.message(Command('about'))
    @router.message(F.text.lower() == "о боте")
    async def about(message: Message):
        await message.answer(
            f"Это простой бот для теста =)",
            parse_mode='Markdown',
            reply_markup=get_main_reply_keyboard()
        )


    return router