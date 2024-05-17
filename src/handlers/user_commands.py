from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f

from motor.core import AgnosticDatabase as MDB

from keyboards import main_kb, inline_builder, ProfileSettings

router = Router()


@router.message(CommandStart())
async def start(message: Message, db: MDB) -> None:
    searchers = await db.users.count_documents({"status": 1})
    await message.reply(
        "<b>☕ Начинай поиск собеседника!</b>\n"
        f"<i>👀 Участников в поиске:</i> <code>{searchers}</code>",
        reply_markup=main_kb
    )


@router.message(or_f(Command("profile"), F.text == "🍪 Профиль"))
async def profile(message: Message, user: dict[str, Any]) -> None:
    option = "🔴" if not user["auto_search"] else "🟢"

    await message.reply(
        f"Привет, <b>{message.from_user.first_name}</b>!",
        reply_markup=inline_builder(
            f"{option} Авто-поиск", ProfileSettings(value="auto_search_toggle").pack()
        )
    )