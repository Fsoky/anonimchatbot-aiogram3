from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

ROOT_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: SecretStr

    MONGO_INITDB_ROOT_USERNAME: str | None = None
    MONGO_INITDB_ROOT_PASSWORD: str | None = None

    ME_CONFIG_BASICAUTH_USERNAME: str | None = None
    ME_CONFIG_BASICAUTH_PASSWORD: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


config = Config()
