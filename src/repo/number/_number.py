from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload

from src.database import new_session, Number


class NumberRepo:
    @staticmethod
    async def add_number(number: str, address: str) -> int:
        async with new_session() as session:
            stmt = (
                insert(Number)
                .values(
                    number=number,
                    address=address
                )
                .returning(Number.id)
            )
            res = await session.execute(stmt)
            await session.commit()

            return res

    @staticmethod
    async def get_number(number: str) -> Number | None:
        async with new_session() as session:
            query = (
                select(Number)
                .where(Number.number == number)
                .options(joinedload(Number.users_numbers))
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_address_by_number(number: str) -> str | None:
        async with new_session() as session:
            query = (
                select(Number.address)
                .where(Number.number == number)
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def delete_number(number: str) -> None:
        async with new_session() as session:
            stmt = (
                delete(Number)
                .where(Number.number == number)
            )
            await session.execute(stmt)
            await session.commit()
