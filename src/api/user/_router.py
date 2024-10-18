from fastapi import APIRouter, status, HTTPException

from sqlalchemy.exc import IntegrityError

from ._schemas import (
    UserResponse,
    UserWalletResponse,
    UserNumbersResponse,
    UserUsernamesResponse,
    UserHistoryResponse,
    AddUserRequest,
    AddUserSwapRequest
)
from src.service.user import UserService
from src.service.token import TokenService

router = APIRouter()


@router.get(
    '/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserResponse,
            'description': 'Returns user data'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    }
)
async def get_user(user_id: int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )

    return UserResponse.model_validate(user, from_attributes=True)


@router.get(
    '/wallet/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserWalletResponse,
            'description': 'Returns user wallet'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    }
)
async def get_user_wallet(user_id: int):
    user_wallet = await UserService.get_user_wallet(user_id)
    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )

    return UserWalletResponse.model_validate(user_wallet, from_attributes=True)


@router.get(
    '/numbers/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserNumbersResponse,
            'description': 'Returns numbers assigned to specified user'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Numbers assigned to specified user not found'
        }
    }
)
async def get_user_numbers(user_id: int):
    user_numbers = await UserService.get_user_numbers(user_id)
    if not user_numbers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Numbers assigned to user {user_id} not found'
        )

    return UserNumbersResponse(
        numbers=user_numbers
    )


@router.get(
    '/usernames/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserUsernamesResponse,
            'description': 'Returns usernames assigned to specified user'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Usernames assigned to specified user not found'
        }
    }
)
async def get_user_usernames(user_id: int):
    user_usernames = await UserService.get_user_usernames(user_id)
    if not user_usernames:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Usernames assigned to user {user_id} not found'
        )

    return UserUsernamesResponse(
        usernames=user_usernames
    )


@router.get(
    '/history/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': UserHistoryResponse,
            'description': 'Returns history of user transactions'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    }
)
async def get_user_history(user_id: int):
    user_wallet = await UserService.get_user_wallet(user_id)
    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )

    user_history = await UserService.get_user_history(user_id)

    return UserHistoryResponse.model_validate(
        user_history, from_attributes=True
    )


@router.post(
    '/',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add new user'
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Specified user is exists'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def add_user(data: AddUserRequest):
    try:
        await UserService.add_user(data.user_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User {data.user_id} is exists'
        )


@router.post(
    '/swap',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add user swap and update user balance'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': ''
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def add_user_swap(data: AddUserSwapRequest):
    user_wallet = await UserService.get_user_wallet(data.user_id)
    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    # to_token_price = await TokenService.get_token_price(data.from_token.lower())
    # if not to_token_price:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail='Error'
    #     )

    if data.from_token == 'TON':
        to_token_price = await TokenService.get_ton_to_usdt_price()
        volume = to_token_price * data.from_amount
    elif data.from_token == 'USDT':
        to_token_price = await TokenService.get_usdt_to_ton_price()
        volume = data.from_amount
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Token {data.from_token.upper()} not found'
        )

    to_amount = data.from_amount * to_token_price

    await UserService.add_user_swap(
        user_id=data.user_id,
        ton_balance=user_wallet.ton_balance,
        usdt_balance=user_wallet.usdt_balance,
        from_token=data.from_token,
        from_amount=data.from_amount,
        to_token=data.to_token,
        to_amount=to_amount,
        volume=volume
    )
