# bot/handlers/one_c_handlers.py

import logging
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot.handlers.models.dynamic_bot_message import DynamicBotMessage
from bot.handlers.models.fork_maker import BaseForkMaker
from bot.handlers.tickets import add_step
from bot.states import OneCStates, TicketStates, FinalStates
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from bot.keyboards import base_buttons
from bot.handlers.utils import default_handle, flash_message


logger = logging.getLogger(__name__)
router = Router()
fork_maker = BaseForkMaker(base_buttons=base_buttons)
bot_message = DynamicBotMessage()


@router.callback_query(F.data == "inc_1c",
        StateFilter(TicketStates.create_ticket, OneCStates.inc_1c))
async def select_category(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call select_category")

    prompt = "Выберите вашу проблему"
    keyboard = fork_maker.build_keyboard()
    await state.set_state(OneCStates.inc_1c)
    await default_handle(callback, state, prompt, keyboard)


@router.callback_query(StateFilter(OneCStates.inc_1c))
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
    next_state = FinalStates.title

    await default_handle(callback, state, prompt, keyboard, next_state)


@fork_maker.register_callback(name="obmen", text="Проблема с обменом")
async def obmen_handler(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call obmen_handler")
    await bot_message.add_field(state, "Категория", "Проблема с проблема с обменом")

    prompt = await bot_message.render(state,
                                      "💬 Введите заголовок заявки"
                                      "(Краткое описание проблемы)"
                                      )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    next_state = FinalStates.title

    await default_handle(callback, state, prompt, keyboard, next_state)


@fork_maker.register_callback(name="new", text="nwe с обменом")
async def obmen_handler_(callback: CallbackQuery, state: FSMContext):
    logger.debug("Call obmen_handler_")
    await bot_message.add_field(state, "Категория", " nwe с обменом")

    prompt = await bot_message.render(state,
                                      "💬 Введите заголовок заявки"
                                      "(Краткое описание проблемы)"
                                      )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    next_state = FinalStates.title

    await default_handle(callback, state, prompt, keyboard, next_state)


@router.message(StateFilter(FinalStates.title))
async def process_title(message: Message , state: FSMContext):
    logger.debug(f"Call process_title")

    text = message.text.strip()
    await message.delete()

    # Валидация
    if len(text) < 10:
        await flash_message(message,
                            f"❗Заголовок:\n{text} - слишком короткий\n"
                            "Минимальная длина 10 символов\n"
                            "Попробуйте еще раз", delay=5)
        # await bot_message.update_message(message, state, "❗Описание слишком короткое")
        return

    # Сохраняем поле в общий шаблон
    await state.update_data(title=text)
    await bot_message.add_field(state, "Заголовок", text)

    # Переход к следующему шагу
    prompt = await bot_message.render(state, "💬 Опишите проблему более подробно")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(FinalStates.title)


@router.message(StateFilter(FinalStates.description))
async def process_description(message: Message , state: FSMContext):
    logger.debug(f"Call process_description")

    text = message.text.strip()
    await message.delete()

    # Валидация
    if len(text) < 10:
        await flash_message(message,
                            f"❗Описание:\n{text} - слишком короткое\n"
                            "Минимальная длина 10 символов\n"
                            "Попробуйте еще раз", delay=5)
        # await bot_message.update_message(message, state, "❗Описание слишком короткое")
        return

    # Сохраняем поле в общий шаблон
    await state.update_data(description=text)
    await bot_message.add_field(state, "Описание", text)

    # await bot_message.update_message(message, state)

    # Переход к следующему шагу
    prompt = await bot_message.render(state, "✅Заявка сформирована")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(FinalStates.confirm)


@router.callback_query(StateFilter(FinalStates.confirm))
async def process_confirm(message: Message , state: FSMContext):
    prompt = await bot_message.render(state, " Заявка сформирована")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[base_buttons])
    await add_step(state, prompt=prompt, keyboard=keyboard)
    await state.set_state(FinalStates.confirm)
