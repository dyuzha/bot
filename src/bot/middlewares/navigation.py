from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Dict, Any, Callable, Awaitable
from bot.states import NavigationState
from aiogram.fsm.context import FSMContext

class NavigationMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        fsm_context: FSMContext = data.get('fsm_context')

        if fsm_context:
            current_state = await fsm_context.get_state()
            user_data = await fsm_context.get_data()

            # Сохраняем предыдущее состояние
            if 'navigation' not in user_data:
                user_data['navigation'] = {}

            if current_state:
                user_data['navigation']['previous_state'] = current_state
                if isinstance(event, Message):
                    user_data['navigation']['previous_message'] = event.text
                elif isinstance(event, CallbackQuery):
                    user_data['navigation']['previous_message'] = event.message.text

                await fsm_context.update_data(**user_data)

        return await handler(event, data)
