from typing import Any
from motor.motor_asyncio import AsyncIOMotorCollection


class BaseRepository[T]:
    collection: AsyncIOMotorCollection
    model: type[T]

    async def one(self, **filters) -> T | None:
        document = await self.collection.find_one(filters)
        return self.model.model_validate(document) if document else None
    
    async def insert(self, model: T) -> T:
        await self.collection.insert_one(model.model_dump(by_alias=True))
        return self.model.model_validate(model)

    async def count(self, **filters) -> int:
        document = await self.collection.count_documents(filters)
        return document

    async def update(self, _id: int, update_filters: dict[str, Any]) -> None:
        await self.collection.update_one({"_id": _id}, update_filters)
    
    async def update_many(self, _ids: list[int], update_filters: dict[str, Any]) -> None:
        await self.collection.update_many({"_id": {"$in": _ids}}, update_filters)