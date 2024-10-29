from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload

from src.database import new_session, MarketNumber, MarketUsername


class MarketRepo:
    @staticmethod
    async def get_numbers() -> list[MarketNumber] | None:
        async with new_session() as session:
            query = select(MarketNumber).options(joinedload(MarketNumber.user_number))
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_usernames() -> list[MarketUsername] | None:
        async with new_session() as session:
            query = select(MarketUsername).options(
                joinedload(MarketUsername.user_username)
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def add_number(user_number_id: int, price: float) -> None:
        async with new_session() as session:
            stmt = insert(MarketNumber).values(
                user_number_id=user_number_id,
                price=price,
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_username(user_username_id: int, price: float) -> None:
        async with new_session() as session:
            stmt = insert(MarketUsername).values(
                user_username_id=user_username_id,
                price=price,
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_number_price(user_number_id: int, price: float) -> None:
        async with new_session() as session:
            stmt = (
                update(MarketNumber)
                .where(MarketNumber.user_number_id == user_number_id)
                .values(price=price)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_username_price(user_username_id: int, price: float) -> None:
        async with new_session() as session:
            stmt = (
                update(MarketUsername)
                .where(MarketUsername.user_username_id == user_username_id)
                .values(price=price)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_number(user_number_id: int) -> None:
        async with new_session() as session:
            stmt = delete(MarketNumber).where(
                MarketNumber.user_number_id == user_number_id
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_username(user_username_id: int) -> None:
        async with new_session() as session:
            stmt = delete(MarketUsername).where(
                MarketUsername.user_username_id == user_username_id
            )
            await session.execute(stmt)
            await session.commit()
