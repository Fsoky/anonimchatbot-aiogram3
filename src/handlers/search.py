from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, or_f

from motor.core import AgnosticDatabase as MDB

from keyboards import reply_builder

router = Router()


@router.message(or_f(Command("search"), F.text == "☕ Искать собеседника"))
async def search_interlocutor(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    pattern = {
        "text": "У вас уже есть собеседник",
        "reply_markup": reply_builder("❌ Отмена")
    }

    if user["status"] == 0:
        interlocutor = await db.users.find_one({"status": 1})
        await db.users.update_one({"_id": user["_id"]}, {"$set": {"status": 1}})

        if not interlocutor:
            pattern["text"] = "Вы начали поиск соперника"
        else:
            pattern["text"] = "Вы нашли собеседника"
            pattern["reply_markup"] = reply_builder("❌ Выйти")
            
            await db.users.update_one(
                {"_id": user["_id"]}, {"$set": {"status": 2, "interlocutor": interlocutor["_id"]}}
            )
            await db.users.update_one(
                {"_id": interlocutor["_id"]}, {"$set": {"status": 2, "interlocutor": user["_id"]}}
            )
            await message.bot.send_message(interlocutor["_id"], **pattern)
    else:
        pattern["text"] = "Вы уже в поиске"
    await message.reply(**pattern)


@router.message(or_f(Command("cancel"), F.text == "❌ Отмена"))
async def cancel_search(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 1:
        await db.users.update_one({"_id": user["_id"]}, {"$set": {"status": 0}})
        await message.reply("Вы отменили поиск", reply_markup=reply_builder("☕ Искать собеседника"))


@router.message(or_f(Command("leave"), F.text == "❌ Выйти"))
async def leave(message: Message, db: MDB) -> None:
    user = await db.users.find_one({"_id": message.from_user.id})
    if user["status"] == 2:
        await message.reply("Вы вышли из чата", reply_markup=reply_builder("☕ Искать собеседника"))
        await message.bot.send_message(
            user["interlocutor"], "Собеседник покинул чат!", reply_markup=reply_builder("☕ Искать собеседника")
        )

        await db.users.update_many(
            {"_id": {"$in": [user["_id"], user["interlocutor"]]}},
            {"$set": {"status": 0, "interlocutor": ""}}
        )