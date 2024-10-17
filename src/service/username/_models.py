from enum import StrEnum
from datetime import datetime

from pydantic import BaseModel, Field


class Status(StrEnum):
    WALLET = 'Wallet'
    MARKET = 'Market'


class Username(BaseModel):
    id: int
    username: str
    address: str
    status: Status


class UsernameWithOwner(Username):
    owner_id: int = Field(serialization_alias='ownerId')


class MarketUsername(UsernameWithOwner):
    price: float
    created_at: datetime = Field(serialization_alias='createdAt')
