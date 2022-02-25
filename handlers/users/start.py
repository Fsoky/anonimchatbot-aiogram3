from aiogram import types

from loader import dp
from keyboards import keyboard


@dp.message_handler(commands=["start", "help", "menu"])
async def main_menu(message: types.Message):
    await message.answer("🍒 Главное меню", reply_markup=keyboard.main_menu)
