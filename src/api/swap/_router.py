from fastapi import APIRouter, status, HTTPException

from ._schemas import FeeResponse, AddSwapRequest
from src.service.swap import SwapService
from src.service.admin import AdminService, FeeType
from src.service.user import UserService
from src.service.token import TokenService

router = APIRouter()


@router.get(
    '/',
    responses={
        status.HTTP_200_OK: {
            'description': 'Swap is OK'
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            'description': 'Swap is unavailable'
        }
    }
)
async def get_is_swap_available():
    res = await SwapService.is_swap_available()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Swap in unavailable'
        )


@router.get(
    '/fee',
    responses={
        status.HTTP_200_OK: {
            'description': 'Returns swap fee'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'No swap fee'
        }
    }
)
async def get_swap_fee():
    fee = await AdminService.get_fee(FeeType.SWAP)
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'No swap fee'
        )

    return FeeResponse(
        fee=fee
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
            'description': 'Some server error occurred'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def add_swap(data: AddSwapRequest):
    user_wallet = await UserService.get_user_wallet(data.user_id)
    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

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

    fee = await AdminService.get_fee(FeeType.SWAP)
    if not fee or fee > 100 or fee < 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred'
        )

    to_amount = data.from_amount * to_token_price

    await UserService.add_user_swap(
        user_id=data.user_id,
        ton_balance=user_wallet.ton_balance,
        usdt_balance=user_wallet.usdt_balance,
        from_token=data.from_token,
        from_amount=data.from_amount,
        to_token=data.to_token,
        to_amount=to_amount - (to_amount * fee / 100),
        volume=volume
    )