from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from fluentogram import TranslatorHub, FluentTranslator
from fluent_compiler.bundle import FluentBundle

ROOT_DIR = Path(__file__).resolve().parents[2]
LOCALES_DIR = ROOT_DIR / "src" / "core" / "locales"


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr

    MONGO_INITDB_ROOT_USERNAME: SecretStr
    MONGO_INITDB_ROOT_PASSWORD: SecretStr

    ME_CONFIG_BASICAUTH_USERNAME: SecretStr
    ME_CONFIG_BASICAUTH_PASSWORD: SecretStr
    
    def set_project_level(self, level: Literal["dev", "prod"]) -> None:
        if level == "prod":
            self.DB_URL = SecretStr(
                f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME.get_secret_value()}"
                f":{self.MONGO_INITDB_ROOT_PASSWORD.get_secret_value()}"
                f"@mongo:27017/"
            )
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


config = Config()

translator_hub = TranslatorHub(
    {
        "ru": ("ru", "en"),
        "en": ("en",),
    },
    [
        FluentTranslator(
            "ru",
            FluentBundle.from_files("ru-RU", [str(LOCALES_DIR / "ru.ftl")])
        ),
        FluentTranslator(
            "en",
            FluentBundle.from_files("ru-RU", [str(LOCALES_DIR / "en.ftl")])
        )
    ]
)