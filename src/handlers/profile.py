from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, or_f

from motor.core import AgnosticDatabase as MDB

from keyboards import inline_builder
from utils import ProfileSettings

router = Router()


@router.message(or_f(Command("profile"), F.text == "🍪 Профиль"))
async def profile(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    option = "🔴" if not user["auto_search"] else "🟢"

    await message.reply(
        f"Привет, <b>{message.from_user.first_name}</b>!",
        reply_markup=inline_builder(
            f"{option} Авто-поиск", ProfileSettings(value="auto_search_toggle").pack()
        )
    )