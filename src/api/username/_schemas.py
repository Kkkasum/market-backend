from datetime import datetime

from pydantic import BaseModel, Field

from src.service.username import UsernameWithOwner


class UsernameResponse(UsernameWithOwner):
    price: float | None = None
    created_at: datetime | None = Field(default=None, serialization_alias='createdAt')


class UsernameByAddressResponse(BaseModel):
    username: str
