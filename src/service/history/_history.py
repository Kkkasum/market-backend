from datetime import datetime

from src.repo.history import HistoryRepo
from ._models import (
    DepositTx,
    WithdrawalTx,
    SwapTx,
    NftDepositTx,
    NftWithdrawalTx,
    MarketOrder,
)


class HistoryService:
    @staticmethod
    async def get_deposits(user_id: int) -> list[DepositTx] | None:
        deposits = await HistoryRepo.get_deposits(user_id)
        if not deposits:
            return

        return [
            DepositTx.model_validate(deposit, from_attributes=True)
            for deposit in deposits
        ]

    @staticmethod
    async def get_deposit_by_tx_hash(tx_hash: str) -> DepositTx | None:
        deposit = await HistoryRepo.get_deposit_by_tx_hash(tx_hash)
        if not deposit:
            return

        return DepositTx.model_validate(deposit, from_attributes=True)

    @staticmethod
    async def get_withdrawals(user_id: int) -> list[WithdrawalTx] | None:
        withdrawals = await HistoryRepo.get_withdrawals(user_id)
        if not withdrawals:
            return

        return [
            WithdrawalTx.model_validate(withdrawal, from_attributes=True)
            for withdrawal in withdrawals
        ]

    @staticmethod
    async def get_swaps(user_id: int) -> list[SwapTx] | None:
        swaps = await HistoryRepo.get_swaps(user_id)
        if not swaps:
            return

        return [SwapTx.model_validate(swap, from_attributes=True) for swap in swaps]

    @staticmethod
    async def get_nft_deposits(user_id: int) -> list[NftDepositTx] | None:
        nft_deposits = await HistoryRepo.get_nft_deposits(user_id)
        if not nft_deposits:
            return

        return [
            NftDepositTx.model_validate(nft_deposit, from_attributes=True)
            for nft_deposit in nft_deposits
        ]

    @staticmethod
    async def get_nft_withdrawals(user_id: int) -> list[NftWithdrawalTx] | None:
        nft_withdrawals = await HistoryRepo.get_nft_withdrawals(user_id)
        if not nft_withdrawals:
            return

        return [
            NftWithdrawalTx.model_validate(nft_withdrawal, from_attributes=True)
            for nft_withdrawal in nft_withdrawals
        ]

    @staticmethod
    async def get_market_orders(user_id: int) -> list[MarketOrder] | None:
        market_orders = await HistoryRepo.get_market_orders(user_id)
        if not market_orders:
            return

        return [
            MarketOrder.model_validate(market_order, from_attributes=True)
            for market_order in market_orders
        ]

    @staticmethod
    async def get_stats(
        start_time: datetime | None = None, end_time: datetime | None = None
    ) -> tuple[int, int, int]:
        return (
            await HistoryRepo.count_withdrawals(start_time, end_time),
            await HistoryRepo.count_deposits(start_time, end_time),
            await HistoryRepo.count_swaps(start_time, end_time),
        )

    @staticmethod
    async def add_withdrawal(
        user_id: int, token: str, amount: float, address: str, tx_hash: str
    ) -> None:
        await HistoryRepo.add_withdrawal(user_id, token, amount, address, tx_hash)

    @staticmethod
    async def add_deposit(
        user_id: int,
        token: str,
        amount: float,
        tx_hash: str,
        created_at: int | None = None,
    ) -> None:
        await HistoryRepo.add_deposit(user_id, token, amount, tx_hash, created_at)

    @staticmethod
    async def add_swap(
        user_id: int,
        from_token: str,
        from_amount: float,
        to_token: str,
        to_amount: float,
        volume: float,
    ) -> None:
        await HistoryRepo.add_swap(
            user_id, from_token, from_amount, to_token, to_amount, volume
        )

    @staticmethod
    async def add_nft_deposit(
        user_id: int, nft_name: str, nft_address: str, tx_hash: str
    ) -> None:
        await HistoryRepo.add_nft_deposit(user_id, nft_name, nft_address, tx_hash)

    @staticmethod
    async def add_nft_withdrawal(
        user_id: int, nft_name: str, nft_address: str, address: str, tx_hash: str
    ) -> None:
        await HistoryRepo.add_nft_withdrawal(
            user_id, nft_name, nft_address, address, tx_hash
        )

    @staticmethod
    async def add_market_order(
        user_id: int, action: str, nft_name: str, nft_address: str, price: float
    ) -> None:
        await HistoryRepo.add_market_order(
            user_id, action, nft_name, nft_address, price
        )
