"""Application settings loaded from environment variables and token file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _read_bot_token() -> str:
    token_file = os.getenv("BOT_TOKEN_FILE", "").strip()
    if not token_file:
        raise RuntimeError("BOT_TOKEN_FILE is not set")

    try:
        bot_token = Path(token_file).read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as error:
        raise RuntimeError(
            f"Cannot read bot token file: {token_file}"
        ) from error

    if not bot_token:
        raise RuntimeError("Bot token file is empty")

    return bot_token


def _parse_id_list(variable_name: str) -> frozenset[int]:
    raw_value = os.getenv(variable_name, "")
    if not raw_value.strip():
        return frozenset()

    try:
        return frozenset(
            int(item.strip())
            for item in raw_value.split(",")
            if item.strip()
        )
    except ValueError as error:
        raise RuntimeError(
            f"{variable_name} must contain integer IDs separated by commas"
        ) from error


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str = field(repr=False)
    allowed_user_ids: frozenset[int]
    allowed_chat_ids: frozenset[int]

    @classmethod
    def from_environment(cls) -> Settings:
        bot_token = _read_bot_token()

        allowed_user_ids = _parse_id_list("ALLOWED_USER_IDS")
        allowed_chat_ids = _parse_id_list("ALLOWED_CHAT_IDS")

        if not allowed_user_ids and not allowed_chat_ids:
            raise RuntimeError(
                "Set at least one ID in ALLOWED_USER_IDS or ALLOWED_CHAT_IDS"
            )

        return cls(
            bot_token=bot_token,
            allowed_user_ids=allowed_user_ids,
            allowed_chat_ids=allowed_chat_ids,
        )

    def is_allowed(self, user_id: int | None, chat_id: int | None) -> bool:
        return (
            user_id in self.allowed_user_ids
            or chat_id in self.allowed_chat_ids
        )