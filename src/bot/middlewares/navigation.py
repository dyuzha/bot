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
        event: CallbackQuery,
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

        if not fsm_context:
            return await handler(event, data)

        current_state = await fsm_context.get_state()
        user_data = await fsm_context.get_data()

        # Инициализация истории
        navigation_data = user_data.get('navigation_data', {'stack': []})
        stack = navigation_data.get('stack', [])

        message_text = event.message.text
        keyboard_dict = event.message.reply_markup.model_dump()

        logger.debug(f"Current state: {current_state}, navigation_data: {navigation_data}")

        # Проверка на повтор
        is_duplicate = (
            stack
            and stack[-1]["state"] == current_state
            and stack[-1]["message"] == message_text
        )

        # Сохраняем текущее состояние в истории
        if current_state and not is_duplicate:
            navigation_data['stack'].append({
                'state': current_state,
                'message': message_text,
                'keyboard': keyboard_dict
            })


            # Ограничиваем историю последними 10 состояниями
            if len(stack) > 10:
                stack = stack[-10:]

            navigation_data["stack"] = stack
            await fsm_context.update_data(navigation_data=navigation_data)

        return await handler(event, data)


class MessageNavigationMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
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

        if not fsm_context:
            return await handler(event, data)

        current_state = await fsm_context.get_state()
        user_data = await fsm_context.get_data()

        # Инициализация истории
        navigation_data = user_data.get('navigation_data', {'stack': []})
        stack = navigation_data.get('stack', [])

        message_text = None
        keyboard_dict = None

        if isinstance(event, Message):
            message_text = event.text
        # logger.debug(f"Current state: {current_state}, navigation_data: {navigation_data}")

        # Проверка на повтор
        is_duplicate = (
            stack
            and stack[-1]["state"] == current_state
            and stack[-1]["message"] == message_text
        )

        # Сохраняем текущее состояние в истории
        if current_state and not is_duplicate:
            navigation_data['stack'].append({
                'state': current_state,
                'message': message_text,
                'keyboard': keyboard_dict
            })


            # Ограничиваем историю последними 10 состояниями
            if len(stack) > 10:
                stack = stack[-10:]

            navigation_data["stack"] = stack
            await fsm_context.update_data(navigation_data=navigation_data)

        return await handler(event, data)


        # logger.debug(f"Call NavigationMiddleware")
        # logger.debug(f"Middleware caught: {type(event).__name__}")  # Отладочный вывод

        # Добавляем отладочный вывод всех доступных ключей
        # logger.debug(f"Available data keys: {list(data.keys())}")

