from pytoniq_core import Address, Cell
from tonutils.client import ToncenterClient
from tonutils.nft import NFT

from src.common import config, USERNAMES_COLLECTION_ADDRESS
from src.repo.username import UsernameRepo
from ._models import Status, UsernameWithOwner, MarketUsername


class UsernameService:
    @staticmethod
    async def add_username(username: str, address: str) -> int:
        return await UsernameRepo.add_username(username, address)

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
                created_at=username.users_usernames.market_username.created_at,
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
        client = ToncenterClient(
            api_key=(
                config.TONCENTER_API_KEY
                if not config.IS_TESTNET
                else config.TONCENTER_API_KEY_TESTNET
            )
        )

        nft = await NFT.get_nft_data(client=client, nft_address=address)
        if nft.collection_address != Address(USERNAMES_COLLECTION_ADDRESS):
            return

        username = (
            Cell.one_from_boc(
                (
                    await client.run_get_method(
                        address=address.to_str(),
                        method_name='get_telemint_token_name',
                        stack=[],
                    )
                )['stack'][0]['value']
            )
            .begin_parse()
            .load_string()
        )

        return username

    @staticmethod
    async def get_address_by_username(username: str) -> str | None:
        return await UsernameRepo.get_address_by_username(username)

    @staticmethod
    async def delete_username(username: str) -> None:
        await UsernameRepo.delete_number(username)
