from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.database import MarketAction


class Tx(BaseModel):
    id: int
    created_at: datetime = Field(serialization_alias='createdAt')


class DepositTx(Tx):
    token: str
    amount: float
    tx_hash: str = Field(serialization_alias='txHash')


class WithdrawalTx(DepositTx):
    address: str


class SwapTx(Tx):
    from_token: str = Field(serialization_alias='fromToken')
    from_amount: float = Field(serialization_alias='fromAmount')
    to_token: str = Field(serialization_alias='toToken')
    to_amount: float = Field(serialization_alias='toAmount')
    volume: float


class RubDepositTx(Tx):
    personal_id: str = Field(exclude=True)
    onlypays_id: str = Field(exclude=True)
    user_id: int = Field(serialization_alias='userId')
    payment_type: str = Field(serialization_alias='paymentType')
    status: str = Field(exclude=True)
    amount_rub: int | None = Field(default=None, serialization_alias='amountRub')
    amount_usdt: float | None = Field(default=None, serialization_alias='amountUsdt')


class NftDepositTx(Tx):
    nft_name: str = Field(serialization_alias='nftName')
    nft_address: str = Field(serialization_alias='nftAddress')
    tx_hash: str = Field(serialization_alias='txHash')


class NftWithdrawalTx(NftDepositTx):
    address: str


class MarketOrder(BaseModel):
    id: int
    action: MarketAction
    nft_name: str = Field(serialization_alias='nftName')
    nft_address: str = Field(serialization_alias='nftAddress')
    price: str
    created_at: datetime = Field(serialization_alias='createdAt')

    model_config = ConfigDict(coerce_numbers_to_str=True)
