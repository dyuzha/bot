from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.text import BACK_KEY, CANCEL_KEY

base_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text=BACK_KEY, callback_data="navigation_back"),
    InlineKeyboardButton(text=CANCEL_KEY, callback_data="cancel")
]


def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать заявку")],
            # [KeyboardButton(text="Мои заявки")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def confirm_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="confirm")
    builder.adjust(1)
    builder.row(*base_buttons)
    return builder.as_markup()


def back_button(extra_buttons: list = None):
    builder = InlineKeyboardBuilder()

    if extra_buttons:
        for btn in extra_buttons:
            builder.button(text=btn['text'], callback_data=btn['data'])

    builder.button(text=BACK_KEY, callback_data="navigation_back")
    builder.adjust(2)
    return builder.as_markup()


def build_menu_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item["text"], callback_data=item["callback"])
    builder.adjust(1)
    builder.row(*base_buttons)
    return builder.as_markup()


def incident_types_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="💻 Проблемы с работой 1С", callback_data="inc_1c")
    builder.button(text="🖥️ Проблема с оборудованием или ПО", callback_data="inc_it")
    builder.adjust(1)
    builder.row(*base_buttons)
    return builder.as_markup()


def request_types_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔧 Запрос по 1С", callback_data="req_1c")
    builder.button(text="👨‍💻 Запросы по сопровождению", callback_data="req_it")
    builder.adjust(1)
    builder.row(*base_buttons)
    return builder.as_markup()
