from fastapi import APIRouter, status, HTTPException

from ._schemas import (
    MarketNumbersResponse,
    MarketUsernamesResponse,
    AddMarketNumberRequest,
    AddMarketUsernameRequest,
    BuyNumberRequest,
    BuyUsernameRequest
)
from src.service.admin import AdminService, CommissionType
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
    },
    status_code=status.HTTP_201_CREATED
)
async def buy_number(data: BuyNumberRequest):
    buy_com, sell_com = (
        await AdminService.get_commission(CommissionType.BUY),
        await AdminService.get_commission(CommissionType.SELL)
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

    if user.ton_balance < number.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has no enough balance'
        )

    owner = await UserService.get_user_wallet(number.owner_id)

    await UserService.update_ton_balance(
        data.user_id, user.ton_balance - (number.price + number.price * buy_com)
    )  # update buyer
    await UserService.update_ton_balance(
        number.owner_id, owner.ton_balance + (number.price + number.price * sell_com)
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
    },
    status_code=status.HTTP_201_CREATED
)
async def buy_username(data: BuyUsernameRequest):
    buy_com, sell_com = (
        await AdminService.get_commission(CommissionType.BUY),
        await AdminService.get_commission(CommissionType.SELL)
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

    if user.ton_balance < username.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has no enough balance'
        )

    owner = await UserService.get_user_wallet(username.owner_id)

    await UserService.update_ton_balance(
        data.user_id, user.ton_balance - (username.price + username.price * buy_com)
    )  # update buyer
    await UserService.update_ton_balance(
        username.owner_id, owner.ton_balance + (username.price + username.price * sell_com)
    )  # update owner

    res = await UserService.update_username_owner(data.user_id, username.id)
    await MarketService.delete_username(res)
