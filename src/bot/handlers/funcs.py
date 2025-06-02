from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.keyboards import back_button
from functools import wraps


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
