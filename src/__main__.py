from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry
from aiogram.enums import ParseMode

from src.bot.handlers import setup_routers, setup_scenes
from src.bot.middlewares import UserMiddleware

from src.core.config import config, translator_hub


async def main() -> None:
    config.set_project_level("dev")
    
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    dp.edited_message.middleware(UserMiddleware())
    dp.include_router(setup_routers())
    
    registry = SceneRegistry(dp)
    registry.add(*setup_scenes())

    await bot.delete_webhook(True)
    await dp.start_polling(bot, translator_hub=translator_hub)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())