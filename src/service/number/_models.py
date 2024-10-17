from enum import StrEnum
from datetime import datetime

from pydantic import BaseModel, Field


class Status(StrEnum):
    WALLET = 'Wallet'
    MARKET = 'Market'


class Number(BaseModel):
    id: int
    number: str
    address: str
    status: Status


class NumberWithOwner(Number):
    owner_id: int = Field(serialization_alias='ownerId')


class MarketNumber(NumberWithOwner):
    price: float
    created_at: datetime = Field(serialization_alias='createdAt')
