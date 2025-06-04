# bot.handlers.final.py

import logging
from aiogram import F, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, InlineKeyboardMarkup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router
from bot.handlers.deffault import BaseStates
from bot.states import FinalStates
from bot.text import *
from bot.keyboards import incident_types_kb, request_types_kb
from bot.handlers.utils import push_to_stack


logger = logging.getLogger(__name__)
router = Router()


# Обработка ввода описания
@router.callback_query(StateFilter(FinalStates.description))
async def process_description(message: Message , state: FSMContext):
    logger.debug(f"Call process_description")
    description = message.text
    # Сообщение пользователя удаляется, а его текст добавляется в прошлое сообщение бота с инлайн кнопками
    if len(description) <= 10:
        # редактируется то сообщение с inline кнопками с пояснением "Введенное описание слишком короткое, попробуйте снова"
        return
    # переход к следующему состоянию


