"""Telegram bot entry point and first handlers."""

from __future__ import annotations

import asyncio
import html
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, Message

from app.config import Settings


def create_router(settings: Settings) -> Router:
    """Create handlers that share the validated application settings."""
    router = Router(name=__name__)

    @router.message(CommandStart())
    async def handle_start(message: Message) -> None:
        user = message.from_user
        if user is None:
            return

        user_id = user.id
        if not settings.is_allowed(user_id=user_id, chat_id=message.chat.id):
            logging.warning(
                "Ignored /start from unauthorized user_id=%s chat_id=%s",
                user_id,
                message.chat.id,
            )
            return

        display_name = html.escape(user.first_name)
        premium_message = (
            "О, у тебя есть премиум ;-)"
            if user.is_premium
            else "О, у тебя нет премиума, нищеброд =)"
        )
        await message.answer(
            f"Привет, {display_name}! {premium_message}",
        )

    return router


async def main() -> None:
    """Configure the bot and start long polling."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    settings = Settings.from_environment()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(create_router(settings))

    await bot.set_my_commands(
        [BotCommand(command="start", description="Запустить бота")]
    )
    logging.info("Starting HardWatchBot in polling mode")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("HardWatchBot stopped")
