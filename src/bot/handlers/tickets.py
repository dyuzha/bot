import logging
from aiogram import F, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.deffault import BaseStates
from bot.handlers.utils import add_step, deffault_handle, register_step
from bot.states import TicketStates
from bot.text import *
from bot.keyboards import incident_types_kb, request_types_kb


logger = logging.getLogger(__name__)
router = Router()


type_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛠 Инцидент", callback_data="incident")],
            [InlineKeyboardButton(text="📝 Запрос", callback_data="request")],
            [InlineKeyboardButton(text=CANCEL_KEY, callback_data="cancel")]
        ]
    )


@router.message(F.text == "Создать заявку", BaseStates.complete_autorisation)
async def init_create_ticket(message: Message, state: FSMContext):
    """Выбрать Инцидент/Запрос"""
    logger.debug(f"Call init_create_ticket")
    prompt = SELECT_WILL_TYPE_TICKET
    keyboard = type_kb

    await state.set_state(TicketStates.have_type)
    await add_step(state, prompt=prompt, keyboard=keyboard)
    await message.answer(prompt, reply_markup=keyboard)


async def process_type(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call process_type")
    prompt = SELECT_WILL_TYPE_TICKET
    keyboard = type_kb

    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(TicketStates.have_type)
    await callback.message.edit_text(prompt, reply_markup=keyboard)


# Обработка выбора "Инцидент"
@router.callback_query(F.data == "incident", StateFilter(TicketStates.have_type))
async def process_incident(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call process_incident")

    prompt = "🛠 Выберите тип инцидента:"
    keyboard = incident_types_kb()

    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(TicketStates.have_incident_type)

    await callback.message.edit_text(prompt, reply_markup=keyboard)
    await callback.answer()


# Обработка выбора "Запрос"
@router.callback_query(F.data == "request", StateFilter(TicketStates.have_type))
async def process_request(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call process_request")

    prompt = "📝 Выберите тип запроса:"
    keyboard = request_types_kb()

    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(TicketStates.have_request_type)

    await callback.message.edit_text(prompt, reply_markup=keyboard)
    await callback.answer()
