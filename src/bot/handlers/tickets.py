import logging
from aiogram import F, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.deffault import BaseStates
from bot.states import TicketStates
from bot.text import *
from bot.keyboards import incident_types_kb, request_types_kb
from bot.handlers.funcs import with_back_button


logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "Создать заявку", BaseStates.complete_autorisation)
async def select_type(message: Message, state: FSMContext):
    """Выбрать Инцидент/Запрос"""
    logger.debug(f"Call select_type")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛠 Инцидент", callback_data="incident")],
            [InlineKeyboardButton(text="📝 Запрос", callback_data="request")],
            [InlineKeyboardButton(text=CANCEL_KEY, callback_data="cancel")]
        ]
    )
    await message.answer(
        SELECT_WILL_TYPE_TICKET,
        reply_markup=keyboard
    )


@router.callback_query(F.data == "incident", StateFilter(BaseStates.complete_autorisation))
@with_back_button
async def process_incident(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call process_incident")
    await state.set_state(TicketStates.incident_type)
    await callback.message.edit_text(
        "🛠 Выберите тип инцидента:",
        reply_markup=incident_types_kb()
    )
    await callback.answer()


# Обработка выбора "Запрос"
@router.callback_query(F.data == "request", StateFilter(BaseStates.complete_autorisation))
@with_back_button
async def process_request(callback: CallbackQuery, state: FSMContext):
    logger.debug(f"Call process_request")
    await state.set_state(TicketStates.request_type)
    await callback.message.edit_text(
        "📝 Выберите тип запроса:",
        reply_markup=request_types_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "cancel")
@with_back_button
async def cancel_creation(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call cancel_creation")
    """Отмена создания заявки"""
    await state.clear()
    await callback.message.edit_text("🚫 Создание заявки отменено")
    await callback.answer()
