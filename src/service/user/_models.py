from pydantic import BaseModel, Field

from src.service.history import (
    DepositTx,
    WithdrawalTx,
    SwapTx,
    NftDepositTx,
    NftWithdrawalTx,
    MarketOrder,
)
from src.service.number import Number
from src.service.username import Username


class UserWallet(BaseModel):
    ton_balance: float = Field(serialization_alias='tonBalance')
    ton_usd_balance: float = Field(serialization_alias='tonUsdBalance')
    usdt_balance: float = Field(serialization_alias='usdtBalance')


class User(UserWallet):
    numbers: list[Number]
    usernames: list[Username]


class UserHistory(BaseModel):
    deposit_txs: list[DepositTx] | None = Field(serialization_alias='depositTxs')
    withdrawal_txs: list[WithdrawalTx] | None = Field(
        serialization_alias='withdrawalTxs'
    )
    swap_txs: list[SwapTx] | None = Field(serialization_alias='swapTxs')
    nft_deposit_txs: list[NftDepositTx] | None = Field(
        serialization_alias='nftDepositTxs'
    )
    nft_withdrawal_txs: list[NftWithdrawalTx] | None = Field(
        serialization_alias='nftWithdrawalTxs'
    )
    market_orders: list[MarketOrder] | None = Field(serialization_alias='marketOrders')
