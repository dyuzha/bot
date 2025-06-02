from aiogram.fsm.state import State, StatesGroup
import logging


logger = logging.getLogger(__name__)  # Используем __name__ для автоматического определения имени модуля

class BaseStates(StatesGroup):
    waiting_autorisation = State()
    complete_autorisation = State()


class TicketStates(StatesGroup):
    type = State()
    incident_type = State()
    request_type = State()

class NavigationState(StatesGroup):
    previous_state = State()
    previous_message = State()
