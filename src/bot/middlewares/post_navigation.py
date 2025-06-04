# bot/middlewares/navigation.py

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Dict, Any, Callable, Awaitable
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
import logging


logger = logging.getLogger(__name__)


class NavigationMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:

        fsm_context = data.get('fsm_context')
        if all(k in data for k in ("fsm_storage", "bot", "event_chat", "event_from_user")):
            key = StorageKey(
                bot_id=data["bot"].id,
                chat_id=data["event_chat"].id,
                user_id=data["event_from_user"].id,
            )
            fsm_context = FSMContext(data["fsm_storage"], key)
            data["fsm_context"] = fsm_context

        return await handler(event, data)
