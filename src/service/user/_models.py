from pydantic import BaseModel, Field

from src.service.number import Number, Status as NumberStatus
from src.service.username import Username, Status as UsernameStatus
from src.service.history import DepositTx, WithdrawalTx, SwapTx


class UserWallet(BaseModel):
    ton_balance: float = Field(serialization_alias='tonBalance')
    ton_usd_balance: float = Field(serialization_alias='tonUsdBalance')
    usdt_balance: float = Field(serialization_alias='usdtBalance')


class User(UserWallet):
    numbers: list[Number]
    usernames: list[Username]


class UserHistory(BaseModel):
    deposit_txs: list[DepositTx] | None = Field(serialization_alias='depositTxs')
    withdrawal_txs: list[WithdrawalTx] | None = Field(serialization_alias='withdrawalTxs')
    swap_txs: list[SwapTx] | None = Field(serialization_alias='swapTxs')
