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


class RubDeposit(BaseModel):
    id: int
    personal_id: str
    onlypays_id: str
    user_id: int
    payment_type: str
    status: str
    amount_rub: int | None = None
    amount_usdt: float | None = None
    created_at: datetime
