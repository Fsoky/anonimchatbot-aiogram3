from aiogram import types

from loader import dp, bot
from utils.db_api import motor_database

from ..users.start import main_menu
from ..users.accounts import account_user, remove_account_action, account_registration_action
from ..communication.chatting import search_interlocutor, stop_search_action, leave_from_chat_action

db = motor_database.DataBase()


@dp.message_handler(content_types=["text", "sticker", "photo", "voice", "document"])
async def content_handler(message: types.Message):
    chat_id = await db.get_chat_info(message.chat.id)

    if message.text == "🍒 Главное меню":
        await main_menu(message)
    if message.text == "🥑 Аккаунт":
        await account_user(message)
    elif message.text == "☕️ Искать собеседника":
        await search_interlocutor(message)
    elif message.text == "💣 Удалить аккаунт":
        await remove_account_action(message)
    elif message.text == "🍷 Зарегистрироваться":
        await account_registration_action(message)
    elif message.text == "📛 Остановить поиск":
        await stop_search_action(message)
    elif message.text == "💔 Покинуть чат":
        await leave_from_chat_action(message)
    elif message.content_type == "sticker":
        try:
            await bot.send_sticker(chat_id=chat_id["interlocutor_chat_id"], sticker=message.sticker["file_id"])
        except TypeError:
            pass
    elif message.content_type == "photo":
        try:
            await bot.send_photo(chat_id=chat_id["interlocutor_chat_id"], sticker=message.photo["file_id"])
        except TypeError:
            pass
    elif message.content_type == "voice":
        try:
            await bot.send_voice(chat_id=chat_id["interlocutor_chat_id"], sticker=message.voice["file_id"])
        except TypeError:
            pass
    elif message.content_type == "document":
        try:
            await bot.send_document(chat_id=chat_id["interlocutor_chat_id"], sticker=message.document["file_id"])
        except TypeError:
            pass
    else:
        try:
            await bot.send_message(text=message.text, chat_id=chat_id["interlocutor_chat_id"])
        except TypeError:
            pass
