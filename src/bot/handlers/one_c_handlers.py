# bot/handlers/one_c_handlers.py

import logging
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot.handlers.models.dynamic_bot_message import DynamicBotMessage
from bot.handlers.models.fork_maker import BaseForkMaker
from bot.handlers.tickets import add_step
from bot.states import OneCStates, TicketStates, FinalStates, BaseStates
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from bot.keyboards import base_buttons
from bot.handlers.utils import default_handle, flash_message


logger = logging.getLogger(__name__)
router = Router()
fork_maker = BaseForkMaker(base_buttons=base_buttons)
bot_message = DynamicBotMessage()


@router.callback_query(F.data == "inc_1c",
        StateFilter(TicketStates.type, OneCStates.inc_1c))
async def select_category(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call select_category")

    prompt = "Выберите вашу проблему"
    keyboard = fork_maker.build_keyboard()
    await state.set_state(OneCStates.inc_1c)
    await default_handle(callback, state, prompt, keyboard)


@router.callback_query(~F.data.in_({"navigation_back", "cancel"}),  # исключаем назад и отмену
    StateFilter(OneCStates.inc_1c)
)
async def callback_dispatcher(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call callback_dispatcher")
    await fork_maker(callback, state)


@fork_maker.register_callback(name="lic", text="Проблема с лицензией")
async def lic_handler(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call lic_handler")
    await bot_message.add_field(state, "Категория", "Проблема с лицензией")

    prompt = await bot_message.render(state,
                                      "💬 Введите заголовок заявки"
                                      "(Краткое описание проблемы)"
                                      )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    await default_handle(callback, state, prompt, keyboard)
    await state.set_state(FinalStates.title)


@fork_maker.register_callback(name="obmen", text="Проблема с обменом")
async def obmen_handler(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call obmen_handler")
    await bot_message.add_field(state, "Категория", "Проблема с проблема с обменом")

    prompt = await bot_message.render(state,
                                      "💬 Введите заголовок заявки"
                                      "(Краткое описание проблемы)"
                                      )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])

    await default_handle(callback, state, prompt, keyboard)
    await state.set_state(FinalStates.title)
