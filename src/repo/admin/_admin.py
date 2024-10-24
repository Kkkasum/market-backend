from sqlalchemy import insert, select, update, delete

from src.database import (
    new_session,
    User, UserStatus,
    FeeType, Fee
)


class AdminRepo:
    @staticmethod
    async def get_fees() -> list[Fee]:
        async with new_session() as session:
            query = select(Fee)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_fee(fee_type: FeeType) -> Fee:
        async with new_session() as session:
            query = (
                select(Fee)
                .where(Fee.type == fee_type)
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def set_fee(fee_type: FeeType, value: int | float) -> None:
        async with new_session() as session:
            stmt = (
                update(Fee)
                .where(Fee.type == fee_type)
                .values(
                    value=value
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def activate_user(user_id: int) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(status=UserStatus.ACTIVE)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def block_user(user_id: int) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(
                    status=UserStatus.BLOCKED
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_user(user_id: int) -> None:
        async with new_session() as session:
            stmt = (
                delete(User)
                .where(User.id == user_id)
            )
            await session.execute(stmt)
            await session.commit()
