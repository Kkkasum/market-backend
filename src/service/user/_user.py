from src.repo.user import UserRepo
from src.service.history import HistoryService
from src.service.token import TokenService
from ._models import (
    NumberStatus,
    UsernameStatus,
    User,
    UserWallet,
    Number,
    Username,
    UserHistory,
)


class UserService:
    @staticmethod
    async def add_user(user_id: int) -> None:
        await UserRepo.add_user(user_id)

    @staticmethod
    async def add_deposit(
        user_id: int,
        ton_balance: float,
        usdt_balance: float,
        token: str,
        amount: float,
        tx_hash: str,
        created_at: int | None = None,
    ) -> None:
        await HistoryService.add_deposit(user_id, token, amount, tx_hash, created_at)

        if token == 'TON':
            await UserRepo.update_user_balance(
                user_id, ton_balance + amount, usdt_balance
            )
        else:
            await UserRepo.update_user_balance(
                user_id, ton_balance, usdt_balance + amount
            )

    @staticmethod
    async def add_withdrawal(
        user_id: int,
        ton_balance: float,
        usdt_balance: float,
        token: str,
        amount: float,
        address: str,
        tx_hash: str,
    ) -> None:
        await HistoryService.add_withdrawal(user_id, token, amount, address, tx_hash)

        if token == 'TON':
            await UserRepo.update_ton_balance(user_id, ton_balance - amount)
        else:
            await UserRepo.update_usdt_balance(user_id, usdt_balance - amount)

    @staticmethod
    async def add_user_swap(
        user_id: int,
        ton_balance: float,
        usdt_balance: float,
        from_token: str,
        from_amount: float,
        to_token: str,
        to_amount: float,
        volume: float,
    ) -> None:
        await HistoryService.add_swap(
            user_id, from_token, from_amount, to_token, to_amount, volume
        )

        if from_token == 'TON' and to_token == 'USDT':
            await UserRepo.update_user_balance(
                user_id, ton_balance - from_amount, usdt_balance + to_amount
            )
        elif from_token == 'USDT' and to_token == 'TON':
            await UserRepo.update_user_balance(
                user_id, ton_balance + to_amount, usdt_balance - from_amount
            )

    @staticmethod
    async def add_user_number(user_id: int, number_id: int) -> None:
        await UserRepo.add_user_number(user_id, number_id)

    @staticmethod
    async def add_user_username(user_id: int, username_id: int) -> None:
        await UserRepo.add_user_username(user_id, username_id)

    @staticmethod
    async def add_user_tron_address(user_id: int, address: str) -> None:
        await UserRepo.add_user_tron_address(user_id, address)

    @staticmethod
    async def get_user(user_id: int) -> User | None:
        user = await UserRepo.get_user(user_id)
        if not user:
            return

        ton_usd_price = await TokenService.get_ton_to_usdt_price()
        ton_usd_balance = user.ton_balance * ton_usd_price

        return User(
            ton_balance=user.ton_balance,
            ton_usd_balance=ton_usd_balance,
            usdt_balance=user.usdt_balance,
            numbers=[
                Number(
                    id=n.number.id,
                    number=n.number.number,
                    address=n.number.address,
                    status=(
                        NumberStatus.MARKET if n.market_number else NumberStatus.WALLET
                    ),
                )
                for n in user.users_numbers
            ],
            usernames=[
                Username(
                    id=n.username.id,
                    username=n.username.username,
                    address=n.username.address,
                    status=(
                        UsernameStatus.MARKET
                        if n.market_username
                        else UsernameStatus.WALLET
                    ),
                )
                for n in user.users_usernames
            ],
        )

    @staticmethod
    async def get_users_ids() -> list[int] | None:
        return await UserRepo.get_users_ids()

    @staticmethod
    async def get_user_wallet(user_id: int) -> UserWallet | None:
        user_wallet = await UserRepo.get_user_wallet(user_id)
        if not user_wallet:
            return

        ton_usd_price = await TokenService.get_ton_to_usdt_price()
        ton_usd_balance = user_wallet.ton_balance * ton_usd_price

        return UserWallet(
            ton_balance=user_wallet.ton_balance,
            ton_usd_balance=ton_usd_balance,
            usdt_balance=user_wallet.usdt_balance,
        )

    @staticmethod
    async def get_user_numbers(user_id: int) -> list[Number] | None:
        user_numbers = await UserRepo.get_user_numbers(user_id)
        if not user_numbers:
            return

        return [
            Number(
                id=user_number.number.id,
                number=user_number.number.number,
                address=user_number.number.address,
                status=(
                    NumberStatus.MARKET
                    if user_number.market_number
                    else NumberStatus.WALLET
                ),
            )
            for user_number in user_numbers
        ]

    @staticmethod
    async def get_user_usernames(user_id: int) -> list[Username] | None:
        user_usernames = await UserRepo.get_user_usernames(user_id)
        if not user_usernames:
            return

        return [
            Username(
                id=user_username.username.id,
                username=user_username.username.username,
                address=user_username.username.address,
                status=(
                    UsernameStatus.MARKET
                    if user_username.market_username
                    else UsernameStatus.WALLET
                ),
            )
            for user_username in user_usernames
        ]

    @staticmethod
    async def get_user_history(user_id: int) -> UserHistory:
        deposits = await HistoryService.get_deposits(user_id)
        withdrawals = await HistoryService.get_withdrawals(user_id)
        swaps = await HistoryService.get_swaps(user_id)

        return UserHistory(
            deposit_txs=deposits,
            withdrawal_txs=withdrawals,
            swap_txs=swaps,
        )

    @staticmethod
    async def get_user_number_id(user_id: int, number_id: int) -> int | None:
        user_number = await UserRepo.get_user_number(user_id, number_id)

        return user_number.id

    @staticmethod
    async def get_user_username_id(user_id: int, username_id: int) -> int | None:
        user_username = await UserRepo.get_user_username(user_id, username_id)

        return user_username.id

    @staticmethod
    async def get_user_tron_address(user_id: int) -> str | None:
        return await UserRepo.get_user_tron_address(user_id)

    @staticmethod
    async def update_ton_balance(user_id: int, new_ton_balance: float) -> None:
        await UserRepo.update_ton_balance(user_id, new_ton_balance)

    @staticmethod
    async def update_number_owner(user_id: int, number_id: int) -> int:
        return await UserRepo.update_number_owner(user_id, number_id)

    @staticmethod
    async def update_username_owner(user_id: int, username_id: int) -> int:
        return await UserRepo.update_username_owner(user_id, username_id)
