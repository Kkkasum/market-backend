from datetime import datetime

from sqlalchemy import String, text, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BIGINT

from ._db import Base
from ._enums import UserStatus, TransactionToken, SwapToken, CommissionType


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.ACTIVE)
    ton_balance: Mapped[float] = mapped_column(server_default=text('0'))
    usdt_balance: Mapped[float] = mapped_column(server_default=text('0'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users_numbers: Mapped[list['UserNumber']] = relationship(
        back_populates='user'
    )

    users_usernames: Mapped[list['UserUsername']] = relationship(
        back_populates='user'
    )


class Number(Base):
    __tablename__ = 'numbers'
    __table_args__ = (
        UniqueConstraint('number'),
        UniqueConstraint('address')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(11))
    address: Mapped[str]

    users_numbers: Mapped['UserNumber'] = relationship(
        back_populates='number'
    )


class Username(Base):
    __tablename__ = 'usernames'
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('address')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    address: Mapped[str]

    users_usernames: Mapped['UserUsername'] = relationship(
        back_populates='username'
    )


class UserAddress(Base):
    __tablename__ = 'users_addresses'
    __table_args__ = (
        UniqueConstraint('address'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    address: Mapped[str]


class UserNumber(Base):
    __tablename__ = 'users_numbers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    number_id: Mapped[int] = mapped_column(ForeignKey('numbers.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(
        back_populates='users_numbers', foreign_keys=[user_id]
    )

    number: Mapped['Number'] = relationship(
        back_populates='users_numbers', foreign_keys=[number_id], lazy='joined'
    )

    market_number: Mapped['MarketNumber'] = relationship(
        back_populates='user_number', lazy='joined'
    )


class UserUsername(Base):
    __tablename__ = 'users_usernames'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    username_id: Mapped[int] = mapped_column(ForeignKey('usernames.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(
        back_populates='users_usernames', foreign_keys=[user_id]
    )

    username: Mapped['Username'] = relationship(
        back_populates='users_usernames', foreign_keys=[username_id], lazy='joined'
    )

    market_username: Mapped['MarketUsername'] = relationship(
        back_populates='user_username', lazy='joined'
    )


class UserDeposit(Base):
    __tablename__ = 'users_deposits'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    token: Mapped[TransactionToken]
    amount: Mapped[float]
    tx_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class UserWithdrawal(Base):
    __tablename__ = 'users_withdrawals'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    token: Mapped[TransactionToken]
    amount: Mapped[float]
    address: Mapped[str]
    tx_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class UserSwap(Base):
    __tablename__ = 'users_swaps'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    from_token: Mapped[SwapToken]
    from_amount: Mapped[float]
    to_token: Mapped[SwapToken]
    to_amount: Mapped[float]
    volume: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class MarketNumber(Base):
    __tablename__ = 'market_numbers'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_number_id: Mapped[int] = mapped_column(ForeignKey('users_numbers.id', ondelete='CASCADE'))
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_number: Mapped['UserNumber'] = relationship(
        back_populates='market_number', foreign_keys=[user_number_id]
    )


class MarketUsername(Base):
    __tablename__ = 'market_usernames'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_username_id: Mapped[int] = mapped_column(ForeignKey('users_usernames.id', ondelete='CASCADE'))
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_username: Mapped['UserUsername'] = relationship(
        back_populates='market_username', foreign_keys=[user_username_id]
    )


class Commission(Base):
    __tablename__ = 'commissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[CommissionType]
    value: Mapped[float] = mapped_column(server_default=text('0'))
