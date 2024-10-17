from sqlalchemy import insert, select, update, delete

from src.database import (
    new_session,
    User, UserStatus,
    CommissionType, Commission
)


class AdminRepo:
    @staticmethod
    async def get_commissions() -> list[Commission]:
        async with new_session() as session:
            query = select(Commission)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_commission(commission_type: CommissionType) -> Commission:
        async with new_session() as session:
            query = (
                select(Commission)
                .where(Commission.type == commission_type)
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def set_commission(commission_type: CommissionType, value: float) -> None:
        async with new_session() as session:
            stmt = (
                update(Commission)
                .where(Commission.type == commission_type)
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
