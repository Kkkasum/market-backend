from datetime import datetime

from pydantic import BaseModel, Field

from src.service.number import NumberWithOwner, Status as NumberStatus
from src.service.username import UsernameWithOwner, Status as UsernameStatus


class MarketAsset(BaseModel):
    price: float
    created_at: datetime = Field(serialization_alias='createdAt')


class MarketNumber(MarketAsset, NumberWithOwner):
    pass


class MarketUsername(MarketAsset, UsernameWithOwner):
    pass
