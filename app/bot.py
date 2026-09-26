"""Telegram bot entry point and first handlers."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.settings.logger import setup_logging
from app.settings.config import AppSettings
from app.handlers.router import create_router

module_logger = logging.getLogger(__name__)


async def main() -> None:
    """Configure the bot and start long polling."""

    setup_logging()

    settings = AppSettings.from_environment()
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(create_router(settings))

    async with bot.context():
        await bot.set_my_commands([
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="about", description="О боте"),
        ])
        module_logger.info("Starting HardWatchBot in polling mode")
        await dispatcher.start_polling(bot, close_bot_session=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        module_logger.info("HardWatchBot stopped")
