from aiogram import Router


def setup_message_routers() -> Router:
    from . import start, search, bot_messages

    router = Router()
    router.include_router(start.router)
    router.include_router(search.router)
    router.include_router(bot_messages.router)
    return router