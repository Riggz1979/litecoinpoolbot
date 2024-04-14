from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_gr_less_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=">")
    kb.button(text="<")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def select_crypto() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="bitcoin")
    kb.button(text="litecoin")
    kb.button(text="dogecoin")
    kb.button(text="ethereum")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
