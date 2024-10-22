from ._models import DepositTx, WithdrawalTx, SwapTx
from src.repo.history import HistoryRepo, TransactionToken, SwapToken


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

        return [
            SwapTx.model_validate(swap, from_attributes=True)
            for swap in swaps
        ]

    @staticmethod
    async def add_withdrawal(user_id: int, token: str, amount: float, address: str, tx_hash: str) -> None:
        await HistoryRepo.add_withdrawal(user_id, token, amount, address, tx_hash)

    @staticmethod
    async def add_deposit(user_id: int, token: str, amount: float, tx_hash: str) -> None:
        await HistoryRepo.add_deposit(user_id, token, amount, tx_hash)

    @staticmethod
    async def add_swap(
        user_id: int,
        from_token: str,
        from_amount: float,
        to_token: str,
        to_amount: float,
        volume: float
    ) -> None:
        await HistoryRepo.add_swap(user_id, from_token, from_amount, to_token, to_amount, volume)
