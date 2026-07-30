from aiogram import Router
from aiogram.fsm.scene import Scene

from . import chat


def setup_routers() -> Router:
    router = Router()

    router.include_router(chat.router)
    return router


def setup_scenes() -> list[type[Scene]]:
    return [
        chat.Chat
    ]