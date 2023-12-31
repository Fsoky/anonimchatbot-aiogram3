from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from motor.core import AgnosticDatabase as MDB


class CheckUser(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        db: MDB = data.get("db")
        
        user = await db.users.find_one({"_id": event.from_user.id})
        if not user:
            return await event.answer("/start")
        return await handler(event, data)