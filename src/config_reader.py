import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

ENV_FILE_DIR = os.path.abspath(".")


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=f"{ENV_FILE_DIR}/.env",
        env_file_encoding="utf-8"
    )


config = Settings()