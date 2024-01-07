from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☕ Искать собеседника")
        ],
        [
            KeyboardButton(text="🍪 Профиль")
        ]
    ],
    resize_keyboard=True
)