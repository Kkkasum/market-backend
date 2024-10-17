from datetime import datetime

from pydantic import BaseModel, Field


class Tx(BaseModel):
    id: int
    created_at: datetime = Field(serialization_alias='createdAt')


class DepositTx(Tx):
    token: str
    amount: float


class WithdrawalTx(DepositTx):
    address: str


class SwapTx(Tx):
    from_token: str = Field(serialization_alias='fromToken')
    from_amount: float = Field(serialization_alias='fromAmount')
    to_token: str = Field(serialization_alias='toToken')
    to_amount: float = Field(serialization_alias='toAmount')
    volume: float
