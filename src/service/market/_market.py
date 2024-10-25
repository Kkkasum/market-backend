from ._models import NumberStatus, UsernameStatus, MarketNumber, MarketUsername
from src.common import r, NUMBERS_COLLECTION_ADDRESS
from src.repo.market import MarketRepo
from src.service.nft import NftService


class MarketService:
    @staticmethod
    async def get_numbers() -> list[MarketNumber] | None:
        numbers = await MarketRepo.get_numbers()
        if not numbers:
            return

        return [
            MarketNumber(
                id=number.user_number.number.id,
                number=number.user_number.number.number,
                address=number.user_number.number.address,
                price=number.price,
                created_at=number.created_at,
                status=NumberStatus.MARKET,
                owner_id=number.user_number.user_id
            )
            for number in numbers
        ]

    @staticmethod
    async def get_usernames() -> list[MarketUsername] | None:
        usernames = await MarketRepo.get_usernames()
        if not usernames:
            return

        return [
            MarketUsername(
                id=username.user_username.username.id,
                username=username.user_username.username.username,
                address=username.user_username.username.address,
                price=username.price,
                created_at=username.created_at,
                status=UsernameStatus.MARKET,
                owner_id=username.user_username.user_id
            )
            for username in usernames
        ]

    @staticmethod
    async def get_instant_sell_number_price() -> float | None:
        price = await r.get('instant_sell_number_price')
        if price:
            return float(price)

        price = await NftService.get_nft_collection_floor_price(NUMBERS_COLLECTION_ADDRESS)
        if not price:
            return

        await r.setex(name='instant_sell_number_price', value=float(price), time=3600)

        return float(price)

    @staticmethod
    async def add_number(user_number_id: int, price: float) -> None:
        await MarketRepo.add_number(user_number_id, price)

    @staticmethod
    async def add_username(user_username_id: int, price: float) -> None:
        await MarketRepo.add_username(user_username_id, price)

    @staticmethod
    async def delete_number(user_number_id: int) -> None:
        await MarketRepo.delete_number(user_number_id)

    @staticmethod
    async def delete_username(user_username_id: int) -> None:
        await MarketRepo.delete_username(user_username_id)
