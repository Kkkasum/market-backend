from datetime import datetime

from sqlalchemy import insert, select, update, func

from src.database import new_session, StartUtime


class AccountRepo:
    @staticmethod
    async def add_start_utime() -> None:
        async with new_session() as session:
            stmt = insert(StartUtime)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_start_utime() -> StartUtime | None:
        async with new_session() as session:
            query = select(StartUtime)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def update_start_utime() -> None:
        async with new_session() as session:
            stmt = (
                update(StartUtime)
                .values(
                    start_utime=func.now()
                )
            )
            await session.execute(stmt)
            await session.commit()
