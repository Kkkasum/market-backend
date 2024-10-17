from sqlalchemy import select, insert

from src.database import new_session, TransactionToken, SwapToken, UserDeposit, UserWithdrawal, UserSwap


class HistoryRepo:
    @staticmethod
    async def get_deposits(user_id: int) -> list[UserDeposit]:
        async with new_session() as session:
            query = (
                select(UserDeposit)
                .where(UserDeposit.user_id == user_id)
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_withdrawals(user_id: int) -> list[UserWithdrawal]:
        async with new_session() as session:
            query = (
                select(UserWithdrawal)
                .where(UserWithdrawal.user_id == user_id)
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_swaps(user_id: int) -> list[UserSwap]:
        async with new_session() as session:
            query = (
                select(UserSwap)
                .where(UserSwap.user_id == user_id)
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def add_deposit(user_id: int, token: str, amount: float) -> None:
        async with new_session() as session:
            stmt = (
                insert(UserDeposit)
                .values(
                    user_id=user_id,
                    token=token,
                    amount=amount
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_withdrawal(user_id: int, token: str, amount: float, address: str) -> None:
        async with new_session() as session:
            stmt = (
                insert(UserWithdrawal)
                .values(
                    user_id=user_id,
                    token=token,
                    amount=amount,
                    address=address
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_swap(
        user_id: int,
        from_token: str,
        from_amount: float,
        to_token: str,
        to_amount: float,
        volume: float
    ) -> None:
        async with new_session() as session:
            stmt = (
                insert(UserSwap)
                .values(
                    user_id=user_id,
                    from_token=from_token,
                    from_amount=from_amount,
                    to_token=to_token,
                    to_amount=to_amount,
                    volume=volume
                )
            )
            await session.execute(stmt)
            await session.commit()
