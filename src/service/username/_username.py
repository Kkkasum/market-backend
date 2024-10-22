from pytoniq_core import Address, Slice, Cell

from ._models import Status, Username, UsernameWithOwner, MarketUsername
from src.common import MAINNET_BALANCER, USERNAMES_COLLECTION_ADDRESS
from src.repo.username import UsernameRepo


class UsernameService:
    @staticmethod
    async def get_username(username: str) -> UsernameWithOwner | None:
        username = await UsernameRepo.get_username(username)
        if not username:
            return

        try:
            owner_id = username.users_usernames.user_id
        except AttributeError:
            owner_id = 1

        if username.users_usernames.market_username:
            return MarketUsername(
                id=username.id,
                username=username.username,
                address=username.address,
                status=Status.MARKET,
                owner_id=owner_id,
                price=username.users_usernames.market_username.price,
                created_at=username.users_usernames.market_username.created_at
            )
        else:
            return UsernameWithOwner(
                id=username.id,
                username=username.username,
                address=username.address,
                status=Status.WALLET,
                owner_id=owner_id,
            )
    
    @staticmethod
    async def get_username_by_address(address: Address) -> int | None:
        async with MAINNET_BALANCER as provider:
            username_nft_data: tuple[
                int, int, Slice, Slice, Cell
            ] = await provider.run_get_method(address=address, method='get_nft_data', stack=[])

            collection_address: Address = username_nft_data[2].load_address()
            if collection_address != USERNAMES_COLLECTION_ADDRESS:
                return

            username = (
                await provider.run_get_method(
                    address=address, method='get_telemint_token_name', stack=[]
                )
            )[0].load_string()

            return username

    @staticmethod
    async def delete_username(username: str) -> None:
        await UsernameRepo.delete_number(username)
