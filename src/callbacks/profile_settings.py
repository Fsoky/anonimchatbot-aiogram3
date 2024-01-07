from aiogram import Router, F
from aiogram.types import CallbackQuery

from motor.core import AgnosticDatabase as MDB

from keyboards import inline_builder
from utils import ProfileSettings

router = Router()


@router.callback_query(ProfileSettings.filter(F.action == "change"))
async def change_profile_settings(query: CallbackQuery, callback_data: ProfileSettings, db: MDB) -> None:
    user = await db.users.find_one({"_id": query.from_user.id})

    if callback_data.value == "auto_search_toggle":
        if user["auto_search"]:
            await db.users.update_one({"_id": user["_id"]}, {"$set": {"auto_search": False}})
            option = "🔴"
        else:
            await db.users.update_one({"_id": user["_id"]}, {"$set": {"auto_search": True}})
            option = "🟢"

        await query.message.edit_reply_markup(
            reply_markup=inline_builder(
                f"{option} Авто-поиск", ProfileSettings(value="auto_search_toggle").pack()
            )
        )
    await query.answer()