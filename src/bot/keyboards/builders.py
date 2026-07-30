from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ButtonStyle

from fluentogram import TranslatorRunner


def chat_markup(i18n: TranslatorRunner, cat: int = 1, **markup_kwargs) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    sizes = [2]
    
    match cat:
        case 1:
            builder.button(text=i18n.search(), style=ButtonStyle.PRIMARY)
        case 2:
            builder.button(text=i18n.leave(), style=ButtonStyle.DANGER)
        case 3:
            builder.button(text=i18n.cancel(), style=ButtonStyle.DANGER)
            
    
    return builder.adjust(*sizes).as_markup(resize_keyboard=True, **markup_kwargs)