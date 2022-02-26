from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from utils.db_api import motor_database
from keyboards import keyboard

db = motor_database.DataBase()


class SetBio(StatesGroup):
    user_bio = State()


@dp.message_handler(commands=["bio", "set_bio", "new_bio", "about_me"])
async def user_bio(message: types.Message):
    if await db.check_exists_user(message.from_user.id):
        await SetBio.user_bio.set()
        await message.answer("Запишите новую информацию о себе.")
    else:
        await message.answer("Вы не зарегистрированны в системе.", reply_markup=keyboard.registration_button)


@dp.message_handler(state=SetBio.user_bio)
async def set_new_user_bio(message: types.Message, state: FSMContext):
    await db.update_user_bio(message.from_user.id, message.text)
    await state.finish()
