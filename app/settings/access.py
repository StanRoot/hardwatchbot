import logging
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from app.settings.config import AppSettings


class AccessMiddleware(BaseMiddleware):
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        chat = data.get("event_chat")

        user_id = user.id if user else None
        chat_id = chat.id if chat else None

        if user is not None and self.settings.is_allowed(
            user_id=user_id,
            chat_id=chat_id,
        ):
            return await handler(event, data)

        logging.warning(
            "Access denied: user_id=%s chat_id=%s",
            user_id,
            chat_id,
        )

        if isinstance(event, CallbackQuery):
            await event.answer("Нет доступа", show_alert=True)

        return None