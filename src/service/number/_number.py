from pytoniq_core import Address, Cell
from tonutils.client import ToncenterClient
from tonutils.nft import NFT

from src.common import config, NUMBERS_COLLECTION_ADDRESS
from src.repo.number import NumberRepo
from ._models import Status, NumberWithOwner, MarketNumber


class NumberService:
    @staticmethod
    async def add_number(number: str, address: str) -> int:
        return await NumberRepo.add_number(number, address)

    @staticmethod
    async def get_number(number: str) -> NumberWithOwner | MarketNumber | None:
        number = await NumberRepo.get_number(number)
        if not number:
            return

        try:
            owner_id = number.users_numbers.user_id
        except AttributeError:
            owner_id = 1

        if number.users_numbers.market_number:
            return MarketNumber(
                id=number.id,
                number=number.number,
                address=number.address,
                status=Status.MARKET,
                owner_id=owner_id,
                price=number.users_numbers.market_number.price,
                created_at=number.users_numbers.market_number.created_at,
            )
        else:
            return NumberWithOwner(
                id=number.id,
                number=number.number,
                address=number.address,
                status=Status.WALLET,
                owner_id=owner_id,
            )

    @staticmethod
    async def get_number_by_address(address: Address) -> str | None:
        client = ToncenterClient(
            api_key=(
                config.TONCENTER_API_KEY
                if not config.IS_TESTNET
                else config.TONCENTER_API_KEY_TESTNET
            )
        )

        nft = await NFT.get_nft_data(client=client, nft_address=address)
        if nft.collection_address != Address(NUMBERS_COLLECTION_ADDRESS):
            return

        number = (
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

        return number

    @staticmethod
    async def get_address_by_number(number: str) -> str | None:
        return await NumberRepo.get_address_by_number(number)

    @staticmethod
    async def delete_number(number: str) -> None:
        await NumberRepo.delete_number(number)
