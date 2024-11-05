from datetime import datetime

from sqlalchemy import select, insert, update

from src.database import (
    new_session,
    UserDeposit,
    UserWithdrawal,
    UserNftDeposit,
    UserNftWithdrawal,
    UserSwap,
    MarketOrder,
    UserRubDeposit,
)


class HistoryRepo:
    @staticmethod
    async def get_deposits(user_id: int) -> list[UserDeposit]:
        async with new_session() as session:
            query = select(UserDeposit).where(UserDeposit.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_deposit_by_tx_hash(tx_hash: str) -> UserDeposit | None:
        async with new_session() as session:
            query = select(UserDeposit).where(UserDeposit.tx_hash == tx_hash)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_nft_deposit_by_tx_hash(tx_hash: str) -> UserNftDeposit | None:
        async with new_session() as session:
            query = select(UserNftDeposit).where(UserNftDeposit.tx_hash == tx_hash)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_withdrawals(user_id: int) -> list[UserWithdrawal]:
        async with new_session() as session:
            query = select(UserWithdrawal).where(UserWithdrawal.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_swaps(user_id: int) -> list[UserSwap]:
        async with new_session() as session:
            query = select(UserSwap).where(UserSwap.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_nft_deposits(user_id: int) -> list[UserNftDeposit]:
        async with new_session() as session:
            query = select(UserNftDeposit).where(UserNftDeposit.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_nft_withdrawals(user_id: int) -> list[UserNftWithdrawal]:
        async with new_session() as session:
            query = select(UserNftWithdrawal).where(
                UserNftWithdrawal.user_id == user_id
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_market_orders(user_id: int) -> list[MarketOrder]:
        async with new_session() as session:
            query = select(MarketOrder).where(MarketOrder.user_id == user_id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_rub_deposit(
        personal_id: str, onlypays_id: str
    ) -> UserRubDeposit | None:
        async with new_session() as session:
            query = select(UserRubDeposit).where(
                UserRubDeposit.personal_id == personal_id,
                UserRubDeposit.onlypays_id == onlypays_id,
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def add_deposit(
        user_id: int,
        token: str,
        amount: float,
        tx_hash: str,
        created_at: int | None = None,
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserDeposit).values(
                user_id=user_id, token=token, amount=amount, tx_hash=tx_hash
            )

            if created_at:
                stmt.values(created_at=created_at)

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_withdrawal(
        user_id: int, token: str, amount: float, address: str, tx_hash: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserWithdrawal).values(
                user_id=user_id,
                token=token,
                amount=amount,
                address=address,
                tx_hash=tx_hash,
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
        volume: float,
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserSwap).values(
                user_id=user_id,
                from_token=from_token,
                from_amount=from_amount,
                to_token=to_token,
                to_amount=to_amount,
                volume=volume,
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_nft_deposit(
        user_id: int, nft_name: str, nft_address: str, tx_hash: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserNftDeposit).values(
                user_id=user_id,
                nft_name=nft_name,
                nft_address=nft_address,
                tx_hash=tx_hash,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_nft_withdrawal(
        user_id: int, nft_name: str, nft_address: str, address: str, tx_hash: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserNftWithdrawal).values(
                user_id=user_id,
                nft_name=nft_name,
                nft_address=nft_address,
                address=address,
                tx_hash=tx_hash,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_market_order(
        user_id: int, action: str, nft_name: str, nft_address: str, price: float
    ) -> None:
        async with new_session() as session:
            stmt = insert(MarketOrder).values(
                user_id=user_id,
                action=action,
                nft_name=nft_name,
                nft_address=nft_address,
                price=price,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_rub_deposit(
        user_id: int, personal_id: str, onlypays_id: str, payment_type: str
    ) -> None:
        async with new_session() as session:
            stmt = insert(UserRubDeposit).values(
                user_id=user_id,
                personal_id=personal_id,
                onlypays_id=onlypays_id,
                payment_type=payment_type,
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_rub_deposit(
        id: int, status: str, amount_rub: int, amount_usdt: float
    ) -> None:
        async with new_session() as session:
            stmt = (
                update(UserRubDeposit)
                .where(UserRubDeposit.id == id)
                .values(status=status, amount_rub=amount_rub, amount_usdt=amount_usdt)
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def count_withdrawals(
        start_time: datetime | None = None, end_time: datetime | None = None
    ) -> int:
        async with new_session() as session:
            query = (
                (
                    select(UserWithdrawal).where(
                        UserWithdrawal.created_at.between(start_time, end_time)
                    )
                )
                if start_time and end_time
                else (select(UserWithdrawal))
            )
            res = (await session.execute(query)).scalars().all()

            return len(res)

    @staticmethod
    async def count_deposits(
        start_time: datetime | None = None, end_time: datetime | None = None
    ) -> int:
        async with new_session() as session:
            query = (
                (
                    select(UserDeposit).where(
                        UserDeposit.created_at.between(start_time, end_time)
                    )
                )
                if start_time and end_time
                else (select(UserDeposit))
            )
            res = (await session.execute(query)).scalars().all()

            return len(res)

    @staticmethod
    async def count_swaps(
        start_time: datetime | None = None, end_time: datetime | None = None
    ) -> int:
        async with new_session() as session:
            query = (
                (
                    select(UserSwap).where(
                        UserSwap.created_at.between(start_time, end_time)
                    )
                )
                if start_time and end_time
                else (select(UserSwap))
            )
            res = (await session.execute(query)).scalars().all()

            return len(res)
