# bot/handlers/one_c_handlers.py

import logging
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot.handlers.models.fork_maker import BaseForkMaker
from bot.handlers.tickets import add_step
from bot.states import OneCStates, TicketStates, UniversalStates
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from bot.keyboards import base_buttons
from bot.handlers.utils import deffault_handle


logger = logging.getLogger(__name__)
router = Router()
fork_maker = BaseForkMaker(base_buttons=base_buttons)


@router.callback_query(StateFilter(OneCStates.process_category))
async def callback_dispatcher(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call callback_dispatcher")
    next_state = OneCStates.have_category

    await fork_maker(callback, state)
    await state.set_state(next_state)


@router.callback_query(F.data == "inc_1c", StateFilter(TicketStates.have_incident_type))
async def select_category(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call select_category")

    prompt = "Выберите вашу проблему"
    keyboard = fork_maker.build_keyboard()
    next_state = OneCStates.process_category

    await add_step(state=state, prompt=prompt, keyboard=keyboard)
    await state.set_state(next_state)
    await callback.message.edit_text(prompt, reply_markup=keyboard)


@fork_maker.register_callback(name="lic", text="Проблема с лицензией")
async def lic_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state()
    prompt="Напишите подробное описание"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    next_state = UniversalStates.description
    await deffault_handle(callback, state, next_state, prompt, keyboard)


@fork_maker.register_callback(name="obmen", text="Проблема с обменом")
async def obmen_handler_(callback: CallbackQuery, state: FSMContext):
    prompt="Напишите подробное описание"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    next_state = UniversalStates.description
    await deffault_handle(callback, state, next_state, prompt, keyboard)


@fork_maker.register_callback(name="new", text="nwe с обменом")
async def obmen_handler(callback: CallbackQuery, state: FSMContext):
    prompt="Напишите подробное описание"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    next_state = UniversalStates.description
    await deffault_handle(callback, state, next_state, prompt, keyboard)


# Обработка ввода описания
@router.message(StateFilter(UniversalStates.description))
async def process_description(message: Message , state: FSMContext):
    logger.debug(f"Call process_description")

    # переход к следующему состоянию
    description = message.text.strip()

    if len(description) <= 10:
        await message.answer(
            "Введенное описание слишком короткое. Пожалуйста, напишите подробнее (не менее 10 символов)."
        )
        return

    # Сохраняем описание в состояние
    await state.update_data(description=description)

    # Удаляем сообщение пользователя (по желанию)
    try:
        await message.delete()
    except Exception:
        pass

    # Достаём предыдущее сообщение бота из стека и редактируем его
    data = await state.get_data()
    stack = data.get("navigation_data", {}).get("stack", [])
    if stack:
        last_bot_msg = stack[-1]
        msg_text = f"{last_bot_msg['message']}\n\n✏️ Описание: {description}"
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id - 1,  # предполагаем, что сообщение бота — предыдущее
            text=msg_text,
            reply_markup=last_bot_msg["keyboard"]
        )

    # Переход к следующему шагу
    await state.set_state(OneCStates.process_category)
