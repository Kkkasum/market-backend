from sqlalchemy import select, update, delete

from src.database import (
    new_session,
    User, UserStatus,
    Const, Constant
)


class AdminRepo:
    @staticmethod
    async def get_constants() -> list[Constant]:
        async with new_session() as session:
            query = select(Constant)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_constant(const: Const) -> Constant:
        async with new_session() as session:
            query = (
                select(Constant)
                .where(Constant.const == const)
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def set_constant(const: Const, value: int | float) -> None:
        async with new_session() as session:
            stmt = (
                update(Constant)
                .where(Constant.const == const)
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
