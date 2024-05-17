from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from motor.core import AgnosticDatabase as MDB


class UserMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        db: MDB = data.get("db")

        user = await db.users.find_one({"_id": event.from_user.id})
        if not user:
            user = await db.users.insert_one({
                "_id": event.from_user.id,
                "auto_search": False,
                "status": 0
            })

        data["user"] = user
        return await handler(event, data)