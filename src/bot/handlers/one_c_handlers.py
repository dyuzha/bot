import logging
from typing import Callable, Dict
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from bot.states import OneCStates, TicketStates, UniversalStates
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.keyboards import base_buttons, incident_types_kb
from bot.utils import push_to_stack


logger = logging.getLogger(__name__)
router = Router()


def build_menu_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item["text"], callback_data=item["callback"])
    builder.adjust(1)
    builder.row(*base_buttons)
    return builder.as_markup()


def generate_menu_items(callback_handlers: Dict[str, dict]) -> list[dict]:
    return [
        {"text": data["text"], "callback": name}
        for name, data in callback_handlers.items()
    ]


class Collector:
    def __init__(self):
        self._handlers: Dict[str, dict] = {}

    def register_callback(self, name: str, text: str = "Нет подписи"):
        def decorator(func: Callable):
            self._handlers[name] = {
                "handler": func,
                "text": text
            }
            return func
        return decorator

    async def __call__(self, callback: CallbackQuery, state: FSMContext):
        handler = self._handlers.get(callback.data)
        if not handler:
            return
        await handler["handler"](callback, state)

    # def build_menu_keyboard(self) -> InlineKeyboardMarkup:
    #     builder = InlineKeyboardBuilder()
    #
    #     for item in self._generate_menu_items():
    #         builder.button(text=item["text"], callback_data=item["callback"])
    #     builder.adjust(1)
    #     builder.row(*base_buttons)
    #     return builder.as_markup()


    def build_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for name, item in self._handlers.items():
            builder.button(text=item["text"], callback_data=name)

        builder.adjust(1)

        builder.row(*base_buttons)
        return builder.as_markup()


    def _generate_menu_items(self) -> list[dict]:
        return [
            {"text": data["text"], "callback": name}
            for name, data in self._handlers.items()
        ]


req_1c_collector = Collector()

# router.callback_query(StateFilter(OneCStates.select_category))(
#     req_1c_collector)

@router.callback_query(StateFilter(OneCStates.select_category))
async def callback_dispatcher(callback: CallbackQuery, state: FSMContext):
    await req_1c_collector(callback, state)


async def handle(callback: CallbackQuery, state: FSMContext, next_state: State,
                 prompt: str, keyboard: InlineKeyboardMarkup):
    await push_to_stack(state, prompt, keyboard=keyboard)
    await state.set_state(next_state)
    await callback.message.edit_text(prompt, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "inc_1c", StateFilter(TicketStates.incident_type))
async def select_category(callback: CallbackQuery, state: FSMContext):
    prompt = "Выберите вашу проблему"
    keyboard = req_1c_collector.build_keyboard()
    next_state = OneCStates.select_category
    await handle(callback, state, next_state, prompt, keyboard)


@req_1c_collector.register_callback(name="lic", text="Проблема с лицензией")
async def lic_handler(callback: CallbackQuery, state: FSMContext):
    prompt="Проблема с лицензией"
    keyboard = incident_types_kb()
    next_state = UniversalStates.description
    await handle(callback, state, next_state, prompt, keyboard)


@req_1c_collector.register_callback(name="obmen", text="Проблема с обменом")
async def obmen_handler_(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Проблема с обменом__")
    await callback.answer()


@req_1c_collector.register_callback(name="new", text="nwe с обменом")
async def obmen_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("ff с обменом__")
    await callback.answer()
