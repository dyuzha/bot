from aiogram.fsm.state import State, StatesGroup
import logging


logger = logging.getLogger(__name__)  # Используем __name__ для автоматического определения имени модуля

class BaseStates(StatesGroup):
    waiting_autorisation = State()
    complete_autorisation = State()


class TicketStates(StatesGroup):
    have_type = State()
    type = State()
    have_incident_type = State()
    have_request_type = State()


class OneCStates(StatesGroup):
    process_category = State()
    have_category = State()



class UniversalStates(StatesGroup):
    title = State()
    description = State()
