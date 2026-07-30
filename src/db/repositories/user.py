from src.db.models import User
from src.db.client import db
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    collection = db.users
    model = User