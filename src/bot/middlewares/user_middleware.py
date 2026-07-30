from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from fluentogram import TranslatorHub

from src.db.repositories import UserRepository
from src.db.models import User


class UserMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        hub: TranslatorHub = data.get("translator_hub")
        repo = UserRepository()

        user = await repo.one(_id=event.from_user.id)
        if not user:
            user = await repo.insert(
                User(id=event.from_user.id, lang=event.from_user.language_code)
            )

        data["user_repo"] = repo
        data["i18n"] = hub.get_translator_by_locale(user.lang)
        
        return await handler(event, data)