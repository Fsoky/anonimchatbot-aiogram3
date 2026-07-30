from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import config

cluster = AsyncIOMotorClient(config.DB_URL.get_secret_value())
db = cluster.anonimdb