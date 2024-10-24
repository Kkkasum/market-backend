from fastapi import APIRouter, status, HTTPException, Query

from ._schemas import (
    InstantSellAsset,
    MarketNumbersResponse,
    MarketUsernamesResponse,
    InstantSellPriceResponse,
    AddMarketNumberRequest,
    AddMarketUsernameRequest,
    BuyNumberRequest,
    BuyUsernameRequest,
    InstantSellNumberRequest,
    InstantSellUsernameRequest
)
from src.common import config
from src.service.wallet import Wallet
from src.service.admin import AdminService, FeeType
from src.service.market import MarketService
from src.service.user import UserService
from src.service.number import NumberService, Status as NumberStatus
from src.service.username import UsernameService, Status as UsernameStatus


router = APIRouter()


@router.get(
    '/numbers',
    responses={
        status.HTTP_200_OK: {
            'model': MarketNumbersResponse,
            'description': 'Returns numbers on market'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Numbers on market not found'
        }
    }
)
async def get_numbers():
    numbers = await MarketService.get_numbers()
    if not numbers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Numbers on market not found'
        )

    return MarketNumbersResponse(
        numbers=numbers
    )


@router.get(
    '/usernames',
    responses={
        status.HTTP_200_OK: {
            'model': MarketUsernamesResponse,
            'description': 'Returns usernames on market'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Usernames on market not found'
        }
    }
)
async def get_usernames():
    usernames = await MarketService.get_usernames()
    if not usernames:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usernames on market not found'
        )

    return MarketUsernamesResponse(
        usernames=usernames
    )


@router.get(
    '/instant-sell/price',
    responses={
        status.HTTP_200_OK: {
            'model': InstantSellPriceResponse,
            'description': 'Returns instant sell price for specified asset'
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            'description': 'Specified asset is invalid'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    }
)
async def get_instant_sell_price(asset: InstantSellAsset = Query()):
    if asset == InstantSellAsset.NUMBER:
        price = await MarketService.get_instant_sell_number_price()
    elif asset == InstantSellAsset.USERNAME:
        price = await MarketService.get_instant_sell_username_price()
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Asset {asset} is invalid'
        )

    if not price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    return InstantSellPriceResponse(
        price=str(price)
    )


@router.post(
    '/add/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add number on market'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified number is not assigned to specified user'
        }
    }
)
async def add_number(data: AddMarketNumberRequest):
    user_number_id = await UserService.get_user_number_id(data.user_id, data.number_id)
    if not user_number_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'Number {data.number} is not assigned to user {data.user_id}'
        )

    await MarketService.add_number(user_number_id, data.price)


@router.post(
    '/add/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add number on market'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified number is not assigned to specified user'
        }
    }
)
async def add_username(data: AddMarketUsernameRequest):
    user_username_id = await UserService.get_user_username_id(data.user_id, data.username_id)
    if not user_username_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'Number {data.username} is not assigned to user {data.user_id}'
        )

    await MarketService.add_username(user_username_id, data.price)


@router.post(
    '/buy/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Assign specified number to specified user'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has no enough balance'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified number or user not found'
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Specified number not on market'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def buy_number(data: BuyNumberRequest):
    buy_fee, sell_fee = (
        await AdminService.get_fee(FeeType.BUY) / 100,
        await AdminService.get_fee(FeeType.SELL) / 100
    )
    if not buy_fee or not sell_fee or buy_fee > 1 or sell_fee > 1 or buy_fee < 0 or sell_fee < 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    number = await NumberService.get_number(data.number)
    if not number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Number {data.number} not found'
        )

    if number.status != NumberStatus.MARKET:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Number {data.number} not on market'
        )

    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    if user.ton_balance < number.price + number.price * buy_fee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has no enough balance'
        )

    owner = await UserService.get_user_wallet(number.owner_id)

    await UserService.update_ton_balance(
        data.user_id, user.ton_balance - (number.price + number.price * buy_fee)
    )  # update buyer
    await UserService.update_ton_balance(
        number.owner_id, owner.ton_balance - (number.price + number.price * sell_fee)
    )  # update owner

    res = await UserService.update_number_owner(data.user_id, number.id)
    await MarketService.delete_number(res)


@router.post(
    '/buy/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Assign specified username to specified user'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has no enough balance'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified username or user not found'
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Specified username not on market'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def buy_username(data: BuyUsernameRequest):
    buy_fee, sell_fee = (
        await AdminService.get_fee(FeeType.BUY) / 100,
        await AdminService.get_fee(FeeType.SELL) / 100
    )
    if not buy_fee or not sell_fee or buy_fee > 1 or sell_fee > 1 or buy_fee < 0 or sell_fee < 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    username = await UsernameService.get_username(data.username)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Username {data.username} not found'
        )

    if username.status != UsernameStatus.MARKET:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Username {data.username} not on market'
        )

    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    if user.ton_balance < username.price + username.price * buy_fee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has no enough balance'
        )

    owner = await UserService.get_user_wallet(username.owner_id)

    await UserService.update_ton_balance(
        data.user_id, user.ton_balance - (username.price + username.price * buy_fee)
    )  # update buyer
    await UserService.update_ton_balance(
        username.owner_id, owner.ton_balance - (username.price + username.price * sell_fee)
    )  # update owner

    res = await UserService.update_username_owner(data.user_id, username.id)
    await MarketService.delete_username(res)


@router.post(
    '/instant-sell/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Instant sells number for specified user'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified number is not assigned to specified user'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def instant_sell_number(data: InstantSellNumberRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    number = await NumberService.get_number(data.number)
    if not number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Number {data.number} not found'
        )

    if data.user_id != number.owner_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'Number {data.number} is not assigned to user {data.user_id}'
        )

    price = await MarketService.get_instant_sell_number_price()
    if not price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    wallet = Wallet(address=config.TON_WALLET_ADDRESS, is_testnet=config.IS_TESTNET)
    balance = await wallet.get_balance()
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    if balance < price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    await UserService.update_number_owner(user_id=0, number_id=number.id)
    await UserService.update_ton_balance(user_id=data.user_id, new_ton_balance=user.ton_balance + price)


@router.post(
    '/instant-sell/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Instant sells number for specified user'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has no enough balance'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified number is not assigned to specified user'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def instant_sell_username(data: InstantSellUsernameRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    username = await UsernameService.get_username(data.username)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Username {data.username} not found'
        )

    if data.user_id != username.owner_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'Username {data.username} is not assigned to user {data.user_id}'
        )

    price = await MarketService.get_instant_sell_username_price()
    if not price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    wallet = Wallet(address=config.TON_WALLET_ADDRESS, is_testnet=config.IS_TESTNET)
    balance = await wallet.get_balance()
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    if balance < price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    await UserService.update_username_owner(user_id=0, username_id=username.id)
    await UserService.update_ton_balance(user_id=data.user_id, new_ton_balance=user.ton_balance + price)


@router.put(
    '/remove/number/{user_id}/{number_id}',
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'Removes specified number from market'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified number not found'
        }
    },
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_number(user_id: int, number_id: int):
    user_number_id = await UserService.get_user_number_id(user_id, number_id)
    if not user_number_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Number not found'
        )

    await MarketService.delete_number(user_number_id)


@router.put(
    '/remove/username/{user_id}/{username_id}',
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'Removes specified username from market'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified username not found'
        }
    },
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_username(user_id: int, username_id: int):
    user_username_id = await UserService.get_user_username_id(user_id, username_id)
    if not user_username_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Username not found'
        )

    await MarketService.delete_username(user_username_id)
