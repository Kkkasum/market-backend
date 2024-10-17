from datetime import datetime

from pydantic import BaseModel, Field

from src.service.number import NumberWithOwner


class NumberResponse(NumberWithOwner):
    price: float | None = None
    created_at: datetime | None = Field(default=None, serialization_alias='createdAt')


class NumberByAddressResponse(BaseModel):
    number: str
