from aiogram import types

from loader import dp
from utils.db_api import motor_database
from keyboards import keyboard

db = motor_database.DataBase()


@dp.message_handler(commands=["account", "acc", "profile"])
async def account_user(message: types.Message):
    result = await db.check_exists_user(message.from_user.id)
    if result:
        account_data = await db.get_data(message.from_user.id)
        text = f"""
        ID: {account_data['user_id']}
        Balance: {account_data['balance']}
        Reputation: {account_data['reputation']}
        Bio: {account_data['bio']}
        """

        await message.answer(text, reply_markup=keyboard.account)
    else:
        await message.answer("Вы не зарегистрированы в системе", reply_markup=keyboard.registration_button)


@dp.message_handler(commands=["remove", "rm", "remove_account"])
async def remove_account_action(message: types.Message):
    result = await db.check_exists_user(message.from_user.id)
    if result:
        await message.answer("Вы действительно желаете удалить свой аккаунт?", reply_markup=keyboard.remove_account)
    else:
        await message.answer("Аккаунта не существует, зарегистрируйтесь.", reply_markup=keyboard.registration_button)


@dp.message_handler(commands=["reg", "registration"])
async def account_registration_action(message: types.Message):
    result = await db.check_exists_user(message.from_user.id)
    if not result:
        await db.add_new_user(message.from_user.id)

        await message.answer("Вы успешно зарегистрировались в системе")
        await account_user(message)
