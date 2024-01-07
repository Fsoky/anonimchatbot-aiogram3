from aiogram import Router

from . import chat_commands


def setup_message_routers() -> Router:
    from . import start, profile, bot_messages

    router = Router()
    router.include_router(start.router)
    router.include_router(chat_commands.router)
    router.include_router(profile.router)
    router.include_router(bot_messages.router)
    return router