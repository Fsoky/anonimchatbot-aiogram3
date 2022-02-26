from motor.motor_asyncio import AsyncIOMotorClient

from data import config


class DataBase:

    def __init__(self):
        self.cluster = AsyncIOMotorClient(config.MONGODB_LINK)

        self.collqueue = self.cluster.anonimdb.queue
        self.collusers = self.cluster.anonimdb.users
        self.collchats = self.cluster.anonimdb.chats

    async def check_exists_user(self, user_id):
        return await self.collusers.count_documents({"user_id": user_id})

    async def get_data(self, user_id):
        return await self.collusers.find_one({"user_id": user_id})

    async def add_new_user(self, user_id):
        await self.collusers.insert_one(
            {
                "user_id": user_id,
                "balance": 0,
                "reputation": 0,
                "bio": "Неизвестный пользователь интернета."
            }
        )

    async def delete_account(self, user_id):
        await self.collusers.delete_one({"user_id": user_id})

    """Methods for chat"""

    async def is_active_chat(self, chat_id):
        return await self.collchats.count_documents({"user_chat_id": chat_id})

    async def is_active_interlocutor(self, chat_id):
        return await self.collqueue.count_documents({"chat_id": chat_id})

    async def find_interlocutor(self):
        return await self.collqueue.find_one({})

    async def add_to_queue(self, chat_id):
        await self.collqueue.insert_one({"chat_id": chat_id})

    async def remove_from_queue(self, chat_id):
        await self.collqueue.delete_one({"chat_id": chat_id})

    async def create_chat_with_user(self, chat_id, interlocutor_chat_id):
        await self.collchats.insert_one(
            {
                "user_chat_id": chat_id,
                "interlocutor_chat_id": interlocutor_chat_id
            }
        )

    async def get_chat_info(self, chat_id):
        return await self.collchats.find_one({"user_chat_id": chat_id})

    async def is_in_the_queue(self, chat_id):
        return await self.collqueue.count_documents({"chat_id": chat_id})

    async def remove_from_chat(self, chat_id):
        await self.collchats.delete_one({"user_chat_id": chat_id})

    async def update_user_bio(self, user_id, content):
        await self.collusers.update_one({"user_id": user_id}, {"$set": {"bio": content}})
