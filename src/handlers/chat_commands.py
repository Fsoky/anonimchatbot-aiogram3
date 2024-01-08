from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, or_f

from motor.core import AgnosticDatabase as MDB

from keyboards import reply_builder, main_kb

router = Router()


@router.message(or_f(Command("search"), F.text == "☕ Искать собеседника"))
async def search_interlocutor(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    pattern = {
        "text": (
            "<b>☕ У тебя уже есть активный чат</b>\n"
            "<i>Используй команду /leave, чтобы покинуть чат</i>"
        ),
        "reply_markup": reply_builder("🚫 Прекратить диалог")
    }

    if user["status"] == 0:
        interlocutor = await db.users.find_one({"status": 1})
        await db.users.update_one({"_id": user["_id"]}, {"$set": {"status": 1}})

        if not interlocutor:
            pattern["text"] = (
                "<b>👀 Ищу тебе собеседника...</b>\n"
                "<i>/cancel - Отменить поиск собеседника</i>"
            )
            pattern["reply_markup"] = reply_builder("❌ Отменить поиск")
        else:
            pattern["text"] = (
                "<b>🎁 Я нашел тебе собеседника, приятного общения!</b>\n"
                "<i>/next - Следующий собеседник</i>\n"
                "<i>/leave - Прекратить диалог</i>"
            )
            pattern["reply_markup"] = reply_builder("🚫 Прекратить диалог")
            
            await db.users.update_one(
                {"_id": user["_id"]}, {"$set": {"status": 2, "interlocutor": interlocutor["_id"]}}
            )
            await db.users.update_one(
                {"_id": interlocutor["_id"]}, {"$set": {"status": 2, "interlocutor": user["_id"]}}
            )
            await message.bot.send_message(interlocutor["_id"], **pattern)
    elif user["status"] == 1:
        pattern["text"] = (
            "<b>👀 УЖЕ ИЩУ тебе собеседника...</b>\n"
            "<i>/cancel - Отменить поиск собеседника</i>"
        )
        pattern["reply_markup"] = reply_builder("❌ Отменить поиск")

    await message.reply(**pattern)


@router.message(or_f(Command("cancel"), F.text == "❌ Отменить поиск"))
async def cancel_search(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 1:
        await db.users.update_one({"_id": user["_id"]}, {"$set": {"status": 0}})
        await message.reply(
            "<b>😔 Все.. больше никого искать не буду!</b>", reply_markup=main_kb
        )


@router.message(or_f(Command(commands=["leave", "stop"]), F.text == "🚫 Прекратить диалог"))
async def leave(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 2:
        await message.reply("<b>💬 Ты покинул чат!</b>", reply_markup=main_kb)
        await message.bot.send_message(
            user["interlocutor"], "<b>💬 Собеседник покинул чат!</b>", reply_markup=main_kb
        )

        await db.users.update_many(
            {"_id": {"$in": [user["_id"], user["interlocutor"]]}},
            {"$set": {"status": 0, "interlocutor": ""}}
        )

        # TODO: Реализовать автопоиск


@router.message(Command("next"))
async def next_interlocutor(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 2:
        await message.bot.send_message(
            user["interlocutor"], "<b>💬 Собеседник покинул чат!</b>", reply_markup=main_kb
        )
        await db.users.update_many(
            {"_id": {"$in": [user["_id"], user["interlocutor"]]}},
            {"$set": {"status": 0, "interlocutor": ""}}
        )

    await search_interlocutor(message, db)