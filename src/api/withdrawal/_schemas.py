from enum import StrEnum

from pydantic import BaseModel, Field


class Network(StrEnum):
    TRON = 'TRON'
    TON = 'TON'


class FeeResponse(BaseModel):
    fee: int


class WithdrawRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    address: str


class WithdrawUsdtRequest(WithdrawRequest):
    amount: float


class WithdrawTonRequest(WithdrawUsdtRequest):
    pass


class WithdrawNumberRequest(WithdrawRequest):
    number: str


class WithdrawUsernameRequest(WithdrawRequest):
    username: str
