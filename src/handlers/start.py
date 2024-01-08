from contextlib import suppress

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from keyboards import main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message, db: MDB) -> None:
    with suppress(DuplicateKeyError):
        await db.users.insert_one({
            "_id": message.from_user.id,
            "auto_search": False,
            "status": 0
        })

    searchers = await db.users.count_documents({"status": 1})
    await message.reply(
        "<b>☕ Начинай поиск собеседника!</b>\n"
        f"<i>👀 Участников в поиске:</i> <code>{searchers}</code>",
        reply_markup=main_kb
    )