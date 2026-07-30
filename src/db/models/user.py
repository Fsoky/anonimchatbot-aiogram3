from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from src.db.utils.enums import Status


class User(BaseModel):
    id: Annotated[int, Field(..., alias="_id")]
    status: Annotated[Status, Field(Status.IDLE)]
    lang: Annotated[str, Field("ru")]
    interlocutor_id: Annotated[int | None, Field(None)]
    
    model_config = ConfigDict(populate_by_name=True, extra="allow")