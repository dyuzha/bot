from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.text import BACK_KEY, CANCEL_KEY


def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать заявку")],
            # [KeyboardButton(text="Мои заявки")]
        ],
        resize_keyboard=True
    )

def back_button(extra_buttons: list = None):
    builder = InlineKeyboardBuilder()

    if extra_buttons:
        for btn in extra_buttons:
            builder.button(text=btn['text'], callback_data=btn['data'])

    builder.button(text=BACK_KEY, callback_data="navigation_back")
    builder.adjust(2)
    return builder.as_markup()



def incident_types_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="💻 Проблемы с работой 1С", callback_data="inc_1c")
    builder.button(text="🖥️ Проблема с оборудованием или ПО", callback_data="inc_it")
    builder.button(text=CANCEL_KEY, callback_data="cancel")
    builder.button(text=BACK_KEY, callback_data="navigation_back")
    return builder.as_markup()

def request_types_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔧 Запрос по 1С", callback_data="req_1c")
    builder.button(text="👨‍💻 Запрос прав доступа", callback_data="req_it")
    builder.button(text=CANCEL_KEY, callback_data="cancel")
    builder.button(text=BACK_KEY, callback_data="navigation_back")
    builder.adjust(1, 2)
    return builder.as_markup()

def incident_1c_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Ошибка лиценщирования", callback_data="inc_1c")
    builder.button(text="🖥️ Проблема с оборудованием или ПО", callback_data="inc_hardware")
    builder.button(text="🌐 Проблема с сетью", callback_data="inc_network")
    builder.button(text=CANCEL_KEY, callback_data="cancel")
    builder.button(text=BACK_KEY, callback_data="navigation_back")
    builder.adjust(1, 2)
    return builder.as_markup()

def incident_it_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔧 Запрос по 1С", callback_data="req_1c")
    builder.button(text="👨‍💻 Запрос прав доступа", callback_data="req_access")
    builder.button(text="📊 Запрос отчетов", callback_data="req_reports")
    builder.button(text=CANCEL_KEY, callback_data="cancel")
    builder.button(text=BACK_KEY, callback_data="navigation_back")
    builder.adjust(1, 2)
    return builder.as_markup()
