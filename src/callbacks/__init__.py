from aiogram import Router


def setup_callbacks_routers() -> Router:
    from . import profile_settings

    router = Router()
    router.include_router(profile_settings.router)
    return router