from aiogram import types

from loader import dp
from utils.db_api import motor_database
from ..users.start import main_menu

db = motor_database.DataBase()


@dp.callback_query_handler(text_contains="remove")
async def process_remove_account(callback: types.CallbackQuery):
        await callback.message.answer("Вы успешно удалили свой аккаунт.")
        await db.delete_account(callback.from_user.id)
        await main_menu(callback.message)


@dp.callback_query_handler(text_contains="cancel")
async def process_cancel(callback: types.CallbackQuery):
    await callback.message.answer("Хорошо, не шути со мной.")
