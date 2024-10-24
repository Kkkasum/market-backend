from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


class TransactionToken(StrEnum):
    TON = 'TON'
    USDT = 'USDT'


class SwapToken(StrEnum):
    TON = 'TON'
    USDT = 'USDT'


class FeeType(StrEnum):
    WITHDRAWAL_TRON = 'WITHDRAWAL_TRON'
    WITHDRAWAL_TON = 'WITHDRAWAL_TON'
    SWAP = 'SWAP'
    BUY = 'BUT'
    SELL = 'SELL'
