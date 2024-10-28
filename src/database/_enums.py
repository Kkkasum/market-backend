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


class MarketAction(StrEnum):
    BUY = 'BUY'
    SELL = 'SELL'


class Const(StrEnum):
    INSTANT_SELL_PERC = 'INSTANT_SELL_PERC'
    MAX_INSTANT_SELL = 'MAX_INSTANT_SELL'
    FEE_WITHDRAWAL_TRON = 'WITHDRAWAL_TRON'
    FEE_WITHDRAWAL_TON = 'WITHDRAWAL_TON'
    FEE_SWAP = 'SWAP'
    FEE_BUY = 'BUT'
    FEE_SELL = 'SELL'
