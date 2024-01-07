from aiogram.filters.callback_data import CallbackData


class ProfileSettings(CallbackData, prefix="profile"):
    action: str = "change"
    value: str | None = None