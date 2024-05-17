import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from motor.motor_asyncio import AsyncIOMotorClient

from handlers import setup_routers
from middlewares import UserMiddleware

from config_reader import config


async def main() -> None:
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    cluster = AsyncIOMotorClient(config.DATABASE_URL.get_secret_value())
    db = cluster.anonimdb

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    dp.include_router(setup_routers())

    await bot.delete_webhook(True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())