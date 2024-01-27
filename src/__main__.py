import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from motor.motor_asyncio import AsyncIOMotorClient

from handlers import setup_message_routers
from callbacks import setup_callbacks_routers

from middlewares import CheckUser

from config_reader import config


async def main() -> None:
    bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    cluster = AsyncIOMotorClient(config.DATABASE_URL.get_secret_value())
    db = cluster.anonimdb

    dp.message.middleware(CheckUser())

    message_routers = setup_message_routers()
    callback_routers = setup_callbacks_routers()
    dp.include_router(message_routers)
    dp.include_router(callback_routers)

    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())