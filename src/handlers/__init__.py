from aiogram import Router

from . import user_commands, profile_settings, chat_commands, bot_messages


def setup_routers() -> Router:
    router = Router()

    router.include_router(user_commands.router)
    router.include_router(chat_commands.router)
    router.include_router(profile_settings.router)
    router.include_router(bot_messages.router)
    return router