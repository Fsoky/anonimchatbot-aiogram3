from aiogram import types

from loader import dp, bot
from utils.db_api import motor_database

from ..users.start import main_menu
from ..users.accounts import account_user, remove_account_action, account_registration_action
from ..communication.chatting import search_interlocutor, stop_search_action, leave_from_chat_action
from ..states.custom_states import user_bio

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
    elif message.text == "💖 Обновить информацию о себе":
        await user_bio(message)

    try:
        if message.content_type == "sticker":
            await bot.send_sticker(chat_id=chat_id["interlocutor_chat_id"], sticker=message.sticker["file_id"])
        elif message.content_type == "photo":
            await bot.send_photo(chat_id=chat_id["interlocutor_chat_id"], photo=message.photo["file_id"])
        elif message.content_type == "voice":
            await bot.send_voice(chat_id=chat_id["interlocutor_chat_id"], voice=message.voice["file_id"])
        elif message.content_type == "document":
            await bot.send_document(chat_id=chat_id["interlocutor_chat_id"], document=message.document["file_id"])
        else:
            await bot.send_message(text=message.text, chat_id=chat_id["interlocutor_chat_id"])
    except TypeError:
        pass
