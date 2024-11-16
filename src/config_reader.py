from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

ROOT_DIR = Path(__file__).parent.parent
print(ROOT_DIR)

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DATABASE_URL: SecretStr
    MONGO_INITDB_ROOT_USERNAME: Optional[str] = None
    MONGO_INITDB_ROOT_PASSWORD: Optional[str] = None
    ME_CONFIG_BASICAUTH_USERNAME: Optional[str] = None
    ME_CONFIG_BASICAUTH_PASSWORD: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


config = Config()