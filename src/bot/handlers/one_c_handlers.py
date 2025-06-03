import logging
from typing import Callable, Dict
from aiogram import F, Router
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot.states import TicketStates
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils import push_to_stack


logger = logging.getLogger(__name__)
router = Router()
cb_req_1c_handlers: Dict[str, dict] = {}


@router.callback_query(
        StateFilter(TicketStates.incident_type))
async def handle_menu_callback(callback: CallbackQuery, state: FSMContext):
    cb_data = callback.data
    handler = cb_req_1c_handlers.get(cb_data)
    if handler:
        await handler(callback, state)
    else:
        # await callback.answer("🚫 Неизвестная команда")
        return


def register_req_1c_callback(name: str, text: str = "Нет подписи"):
    def decorator(func: Callable):
        cb_req_1c_handlers[name] = {
            "handler": func,
            "text": text
        }
        return func
    return decorator

def generate_req_1c_menu_items() -> list[dict]:
    return [
        {"text": data["text"], "callback": name}
        for name, data in cb_req_1c_handlers.items()
    ]

def build_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in generate_req_1c_menu_items():
        builder.button(text=item["text"], callback_data=item["callback"])
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(F.data == "inc_1c", StateFilter(TicketStates.incident_type))
async def select_category(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call select_category")
    await state.set_state(TicketStates.select_type)
    await callback.message.edit_text(
        "🛠 Выберите тип инцидента:",
        reply_markup=build_menu_keyboard()
    )
    await callback.answer()


@register_req_1c_callback(name="lic", text="Проблема с лицензией")
async def lic_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Проблема с лицензией__")
    await callback.answer()

@register_req_1c_callback(name="obmen", text="Проблема с обменом")
async def obmen_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Проблема с обменом")
    await callback.answer()

