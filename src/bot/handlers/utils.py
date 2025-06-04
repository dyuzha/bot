# bot/handlers/utils.py

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from bot.keyboards import back_button
from functools import wraps
from typing import Callable, Optional, Awaitable, Any


async def add_step(state: FSMContext, prompt: str, keyboard=None):
    navigation_data = (await state.get_data()).get("navigation_data", {"stack": []})
    stack = navigation_data.get("stack", [])

    stack.append({
        "state": await state.get_state(),
        "message": prompt,
        "keyboard": keyboard.model_dump() if keyboard else None,
    })

    if len(stack) > 10:
        stack = stack[-10:]

    navigation_data["stack"] = stack
    await state.update_data(navigation_data=navigation_data)

async def deffault_handle(callback: CallbackQuery, state: FSMContext, next_state: State,
                 prompt: str, keyboard: InlineKeyboardMarkup):
    await add_step(state=state, prompt=prompt, keyboard=keyboard)
    await state.set_state(next_state)
    await callback.message.edit_text(prompt, reply_markup=keyboard)
    await callback.answer()


def register_step(prompt: str, keyboard: Optional[InlineKeyboardMarkup] = None):
    def decorator(func: Callable[[Message, FSMContext], Awaitable[Any]]):
        @wraps(func)
        async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
            # Выполняем оригинальный хендлер
            result = await func(message, state, *args, **kwargs)

            # Добавляем в стек шаг после выполнения хендлера
            navigation_data = (await state.get_data()).get("navigation_data", {"stack": []})
            stack = navigation_data.get("stack", [])

            stack.append({
                "state": await state.get_state(),
                "message": prompt,
                "keyboard": keyboard.model_dump() if keyboard else None,
            })

            # Ограничиваем стек
            if len(stack) > 10:
                stack = stack[-10:]

            navigation_data["stack"] = stack
            await state.update_data(navigation_data=navigation_data)

            return result
        return wrapper
    return decorator



def with_back_button(func):
    @wraps(func)  # Сохраняем метаданные функции
    async def wrapper(message: Message | CallbackQuery, *args, **kwargs):
        # Пропускаем state и другие параметры
        result = await func(message, *args, **kwargs)

        # Добавляем кнопку "Назад" только для новых сообщений
        if isinstance(message, Message):
            await message.edit_reply_markup(reply_markup=back_button())
        return result
    return wrapper

def generate_menu_items(callback_handlers: dict[str, dict]) -> list[dict]:
    return [
        {"text": data["text"], "callback": name}
        for name, data in callback_handlers.items()
    ]


async def push_to_stack(fsm: FSMContext, text: str, keyboard: Optional[InlineKeyboardMarkup] = None):
    user_data = await fsm.get_data()
    navigation_data = user_data.get("navigation_data", {"stack": []})

    navigation_data["stack"].append({
        "state": await fsm.get_state(),
        "message": text,
        "keyboard": keyboard.model_dump() if keyboard else None
    })

    if len(navigation_data["stack"]) > 10:
        navigation_data["stack"] = navigation_data["stack"][-10:]

    await fsm.update_data(navigation_data=navigation_data)

