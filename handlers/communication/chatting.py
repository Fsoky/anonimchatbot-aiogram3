from aiogram import types

from loader import dp
from utils.db_api import motor_database
from keyboards import keyboard

db = motor_database.DataBase()


@dp.message_handler(commands=["search", "search_user"])
async def search_interlocutor(message: types.Message):
    if message.chat.type == "private":
        if await db.check_exists_user(message.from_user.id):

            if not await db.is_active_chat(message.chat.id):
                interlocutor = await db.find_interlocutor()
                if interlocutor is None:
                    await db.add_to_queue(message.chat.id)
                    await message.answer("🕒 Поиск собеседника начался, пожалуйста подождите...", reply_markup=keyboard.stop_search)
                else:
                    if await db.is_active_interlocutor(interlocutor["chat_id"]):
                        await db.remove_from_queue(message.chat.id)
                        await db.remove_from_queue(interlocutor["chat_id"])

                        await db.create_chat_with_user(message.chat.id, interlocutor["chat_id"])
                        await db.create_chat_with_user(interlocutor["chat_id"], message.chat.id)

                        chat_info = await db.get_chat_info(message.chat.id)
                        default_text = "Собеседник найден! Можете приступить к общению."

                        await message.answer(default_text, reply_markup=keyboard.leave)
                        await dp.bot.send_message(text=default_text, chat_id=chat_info["interlocutor_chat_id"], reply_markup=keyboard.leave)
                    else:
                        await db.add_to_queue(message.chat.id)
                        await message.answer("🕒 Поиск собеседника начался, пожалуйста подождите...", reply_markup=keyboard.stop_search)
            else:
                await message.answer("Вы уже состоите в чате с пользователем.")
        else:
            await message.answer("Вы не зарегистрированы в системе.", reply_markup=keyboard.registration_button)


@dp.message_handler(commands=["stop", "stop_search"])
async def stop_search_action(message: types.Message):
    if await db.is_in_the_queue(message.chat.id):
        await db.remove_from_queue(message.chat.id)
        await message.answer("Вы были исключены из очереди.", reply_markup=keyboard.main_menu)
    else:
        await message.answer("Вы не состоите в очереди.")


@dp.message_handler(commands=["leave", "leave_chat"])
async def leave_from_chat_action(message: types.Message):
    if await db.is_active_chat(message.chat.id):
        chat_info = await db.get_chat_info(message.chat.id)

        await message.answer("Вы покинули чат.", reply_markup=keyboard.main_menu)
        await dp.bot.send_message(text="Собеседник покинул чат.", chat_id=chat_info["interlocutor_chat_id"], reply_markup=keyboard.main_menu)

        await db.remove_from_chat(chat_info["interlocutor_chat_id"])
        await db.remove_from_chat(message.chat.id)
    else:
        await message.answer("Вы не создавали чат.")
