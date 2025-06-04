from aiogram.fsm.state import State, StatesGroup
import logging


logger = logging.getLogger(__name__)  # Используем __name__ для автоматического определения имени модуля

class BaseStates(StatesGroup):
    waiting_autorisation = State()
    complete_autorisation = State()

class TicketStates(StatesGroup):
    create_ticket = State()

class OneCStates(StatesGroup):
    inc_1c = State()

class FinalStates(StatesGroup):
    description = State()
    title = State()
    confirm = State()
