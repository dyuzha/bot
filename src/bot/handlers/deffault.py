import logging
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from bot.keyboards import main_kb
from aiogram.fsm.context import FSMContext
from bot.states import BaseStates


logger = logging.getLogger(__name__)
router = Router()


START_MESSAGE = (
    "👋 Привет! Я ПРОФИТ-бот для работы с GLPI.\n"
    "С моей помощью вы можете создать заявку."
)

AUTH_REQUIRED_MESSAGE = (
    "Для продолжения взаимодействия с ботом необходима авторизация\n"
    "Введите свой логин, используемый в вашей организации "
    "(например: <code>ivanov_ii</code>):"
)

def check_register(id):
    """Реализация будет потом"""
    user_id = 1
    login = 1
    if login is None:
        logger.info(f"User {user_id} needs authorization")
        return False
    return True


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await main_menu(message, state)


async def main_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if check_register(id) is None:
        await state.set_state(BaseStates.waiting_autorisation)
        await message.answer(AUTH_REQUIRED_MESSAGE, reply_markup=main_kb())
        return
    await state.set_state(BaseStates.complete_autorisation)
    await message.answer(START_MESSAGE, reply_markup=main_kb())
