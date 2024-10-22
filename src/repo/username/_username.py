from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload

from src.database import new_session, Username


class UsernameRepo:
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
    async def delete_number(username: str) -> None:
        async with new_session() as session:
            stmt = (
                delete(Username)
                .where(Username.username == username)
            )
            await session.execute(stmt)
            await session.commit()
