from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

class DynamicBotMessage:
    def __init__(self, head: str = "📝 Детали заявки", separator: str = "\n\n"):
        self.head = head
        self.separator = separator

    async def add_field(self, state: FSMContext, key: str, value: str):
        """
        Добавляет или обновляет поле в хранилище состояния.
        key — имя поля (например, 'Описание')
        value — значение поля (например, 'У нас сломалась 1С')
        """
        data = await state.get_data()
        fields = data.get("dynamic_fields", {})
        fields[key] = value
        await state.update_data(dynamic_fields=fields)

    async def render(self, state: FSMContext, *strings) -> str:
        """
        Генерирует текст сообщения на основе всех сохранённых полей и
        дополнительных строк
        Возвращает строку для передачи в edit_message_text.
        """
        data = await state.get_data()
        fields = data.get("dynamic_fields", {})

        parts = [self.head]
        parts.extend(f"{key}: {value}" for key, value in fields.items())
        parts.extend(s for s in strings if s)

        return self.separator.join(parts)

    async def update_message(self, message: Message, state: FSMContext, *strings):
        """
        Редактирует последнее сообщение бота, извлекая его из navigation-стека.
        Используется для отображения обновлённой информации пользователю.
        """
        data = await state.get_data()
        stack = data.get("navigation_data", {}).get("stack", [])

        if not stack:
            return

        last_bot_msg = stack[-1]
        message_id = last_bot_msg.get("message_id", message.message_id - 1)
        keyboard: InlineKeyboardMarkup = last_bot_msg.get("keyboard")

        text = await self.render(state, strings)

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard,
        )

    async def reset(self, state: FSMContext):
        """Очищает все динамические поля"""
        await state.update_data(dynamic_fields={})
