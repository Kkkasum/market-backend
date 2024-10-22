from pytoniq_core import Slice, Cell, Address

from ._models import Status, Number, NumberWithOwner, MarketNumber
from src.common import MAINNET_BALANCER, NUMBERS_COLLECTION_ADDRESS
from src.repo.number import NumberRepo


class NumberService:
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
                created_at=number.users_numbers.market_number.created_at
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
        async with MAINNET_BALANCER as provider:
            number_nft_data: tuple[
                int, int, Slice, Slice, Cell
            ] = await provider.run_get_method(address=address, method='get_nft_data', stack=[])

            collection_address: Address = number_nft_data[2].load_address()
            if collection_address != NUMBERS_COLLECTION_ADDRESS:
                return

            number = (
                await provider.run_get_method(address=address, method='get_telemint_token_name', stack=[])
            )[0].load_string()

            return number

    @staticmethod
    async def delete_number(number: str) -> None:
        await NumberRepo.delete_number(number)
