from pydantic import BaseModel, Field

from src.service.market import MarketNumber, MarketUsername


class MarketNumbersResponse(BaseModel):
    numbers: list[MarketNumber]


class MarketUsernamesResponse(BaseModel):
    usernames: list[MarketUsername]


class AddMarketNumberRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    number_id: int = Field(validation_alias='numberId')
    number: str
    price: float


class AddMarketUsernameRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    username_id: int = Field(validation_alias='usernameId')
    username: str
    price: float


class BuyNumberRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    number: str


class BuyUsernameRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    username: str
