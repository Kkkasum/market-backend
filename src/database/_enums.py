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


class CommissionType(StrEnum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    SWAP = 'SWAP'
    BUY = 'BUT'
    SELL = 'SELL'
