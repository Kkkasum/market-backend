from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


class PaymentType(StrEnum):
    CARD = 'CARD'
    SPB = 'SPB'


class DepositStatus(StrEnum):
    WAITING = 'waiting'
    SUCCESS = 'success'


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
    FEE_RUB_DEPOSIT = 'FEE_RUB_DEPOSIT'
    FEE_WITHDRAWAL_TRON = 'WITHDRAWAL_TRON'
    FEE_WITHDRAWAL_TON = 'WITHDRAWAL_TON'
    FEE_SWAP = 'SWAP'
    FEE_BUY = 'BUY'
    FEE_SELL = 'SELL'
