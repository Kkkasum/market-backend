from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload, selectinload

from src.database import new_session, User, UserNumber, UserUsername, UserAddress


class UserRepo:
    @staticmethod
    async def add_user(user_id: int) -> None:
        async with new_session() as session:
            stmt = insert(User).values(id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_user_number(user_id: int, number_id: int) -> None:
        async with new_session() as session:
            stmt = insert(UserNumber).values(user_id=user_id, number_id=number_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_user_username(user_id: int, username_id: int) -> None:
        async with new_session() as session:
            stmt = insert(UserUsername).values(user_id=user_id, username_id=username_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_user_tron_address(user_id: int, address: str) -> None:
        async with new_session() as session:
            stmt = insert(UserAddress).values(user_id=user_id, address=address)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_user(user_id: int) -> User | None:
        async with new_session() as session:
            query = (
                select(User)
                .where(User.id == user_id)
                .options(
                    selectinload(User.users_numbers), selectinload(User.users_usernames)
                )
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_users_ids() -> list[int] | None:
        async with new_session() as session:
            query = select(User.id)
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_user_wallet(user_id: int) -> User | None:
        async with new_session() as session:
            query = select(User).where(User.id == user_id)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_numbers(user_id: int) -> list[UserNumber] | None:
        async with new_session() as session:
            query = (
                select(UserNumber)
                .where(UserNumber.user_id == user_id)
                .options(joinedload(UserNumber.number))
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_user_usernames(user_id: int) -> list[UserUsername] | None:
        async with new_session() as session:
            query = (
                select(UserUsername)
                .where(UserUsername.user_id == user_id)
                .options(joinedload(UserUsername.username))
            )
            res = (await session.execute(query)).scalars().all()

            return res

    @staticmethod
    async def get_user_number(user_id: int, number_id: int) -> UserNumber | None:
        async with new_session() as session:
            query = select(UserNumber).where(
                UserNumber.user_id == user_id, UserNumber.number_id == number_id
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_username(user_id: int, username_id: int) -> UserUsername | None:
        async with new_session() as session:
            query = select(UserUsername).where(
                UserUsername.user_id == user_id, UserUsername.username_id == username_id
            )
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def get_user_tron_address(user_id: int) -> str | None:
        async with new_session() as session:
            query = select(UserAddress.address).where(UserAddress.user_id == user_id)
            res = (await session.execute(query)).scalar_one_or_none()

            return res

    @staticmethod
    async def update_user_balance(
        user_id: int, ton_balance: float, usdt_balance: float
    ) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(ton_balance=ton_balance, usdt_balance=usdt_balance)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_ton_balance(user_id: int, new_ton_balance: float) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(
                    ton_balance=new_ton_balance,
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_usdt_balance(user_id: int, new_usdt_balance: float) -> None:
        async with new_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(
                    usdt_balance=new_usdt_balance,
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_number_owner(user_id: int, number_id: int) -> int:
        async with new_session() as session:
            stmt = (
                update(UserNumber)
                .where(UserNumber.number_id == number_id)
                .values(user_id=user_id)
                .returning(UserNumber.id)
            )
            res = (await session.execute(stmt)).scalar()
            await session.commit()

            return res

    @staticmethod
    async def update_username_owner(user_id: int, username_id: int) -> int:
        async with new_session() as session:
            stmt = (
                update(UserUsername)
                .where(UserUsername.username_id == username_id)
                .values(user_id=user_id)
                .returning(UserUsername.id)
            )
            res = (await session.execute(stmt)).scalar()
            await session.commit()

            return res
