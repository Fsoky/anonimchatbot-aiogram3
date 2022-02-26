from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# Клавиатура для главного меню
main_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("🥑 Аккаунт"),
            KeyboardButton("☕️ Искать собеседника")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура для аккаунта
account = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("💣 Удалить аккаунт"),
            KeyboardButton("🍒 Главное меню")
        ],
        [
            KeyboardButton("💖 Обновить информацию о себе")
        ]
    ],
    resize_keyboard=True
)

# Кнопка для регистрации
registration_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("🍷 Зарегистрироваться")
        ]
    ],
    resize_keyboard=True
)

# Клавиатура для удаления аккаунта
remove_account = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да, я согласен", callback_data="remove"),
            InlineKeyboardButton("Нет, я отказываюсь", callback_data="cancel")
        ]
    ],
    one_time_keyboard=True
)

# Кнопка для остановки поиска чата
stop_search = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("📛 Остановить поиск")
        ]
    ],
    resize_keyboard=True
)

# Кнопка для ухода из чата
leave = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("💔 Покинуть чат")
        ]
    ],
    resize_keyboard=True
)
