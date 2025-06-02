from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Dict, Any, Callable, Awaitable
from bot.states import NavigationState
from aiogram.fsm.context import FSMContext
import logging

logger = logging.getLogger(__name__)


class NavigationMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:

        # logger.debug(f"Call NavigationMiddleware")
        logger.debug(f"Middleware caught: {type(event).__name__}")  # Отладочный вывод

        # Добавляем отладочный вывод всех доступных ключей
        logger.debug(f"Available data keys: {list(data.keys())}")

        fsm_context = data.get('fsm_context')

        if not fsm_context:
            logger.debug(f"No context")
            return await handler(event, data)

        current_state = await fsm_context.get_state()
        user_data = await fsm_context.get_data()

        # Инициализация истории
        navigation_data = user_data.get('navigation_data', {'stack': []})

        keyboard = None
        if isinstance(event, Message):
            message_text = event.text
        elif isinstance(event, CallbackQuery):
            message_text = event.message.text
            keyboard = event.message.reply_markup
        else:
            message_text = str(event)

        logger.debug(f"Current state: {current_state}, User data: {user_data['navigation_data']}")

        # Сохраняем текущее состояние в истории
        if current_state:
            navigation_data['stack'].append({
                'state': current_state,
                'message': message_text,
                'keyboard': keyboard
            })

            # Ограничиваем историю последними 10 состояниями
            if len(navigation_data['stack']) > 10:
                navigation_data['stack'] = navigation_data['stack'][-10:]

            await fsm_context.update_data(navigation_data=navigation_data)

        return await handler(event, data)
