from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Меню бота"),
            types.BotCommand("help", "Навигация пом командам"),
            types.BotCommand("search", "Поиск собеседника"),
            types.BotCommand("account", "Ваш аккаунт"),
            types.BotCommand("remove", "Удалить аккаунт"),
            types.BotCommand("registration", "Зарегистрироваться"),
            types.BotCommand("stop", "Остановить поиск"),
            types.BotCommand("leave", "Покинуть чат"),
            types.BotCommand("bio", "Обновить информацию о себе")
        ]
    )
