from sqlalchemy import select, insert, delete
from sqlalchemy.orm import joinedload

from src.database import new_session, Username


class UsernameRepo:
    @staticmethod
    async def add_username(username: str, address: str) -> int:
        async with new_session() as session:
            stmt = (
                insert(Username)
                .values(username=username, address=address)
                .returning(Username.id)
            )
            res = (await session.execute(stmt)).scalar()
            await session.commit()

            return res

    @staticmethod
    async def get_username(username: str) -> Username | None:
        async with new_session() as session:
            query = (
                select(Username)
                .where(Username.username == username)
                .options(joinedload(Username.users_usernames))
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_address_by_username(username: str) -> str | None:
        async with new_session() as session:
            query = select(Username.address).where(Username.username == username)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def delete_number(username: str) -> None:
        async with new_session() as session:
            stmt = delete(Username).where(Username.username == username)
            await session.execute(stmt)
            await session.commit()
