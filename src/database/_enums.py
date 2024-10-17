from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


class TransactionToken(StrEnum):
    TON = 'TON'
    USDT_TON = 'USDT-TON'
    USDT_TRC = 'USDT-TRC'


class SwapToken(StrEnum):
    TON = 'TON'
    USDT = 'USDT'


class CommissionType(StrEnum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    SWAP = 'swap'
    BUY = 'buy'
    SELL = 'sell'
