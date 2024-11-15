from fastapi import APIRouter, status, HTTPException

from src.common import config
from src.service.admin import AdminService, Const
from src.service.swap import SwapService
from src.service.token import TokenService
from src.service.user import UserService
from ._schemas import FeeResponse, AddSwapRequest

router = APIRouter()


@router.get(
    '/',
    responses={
        status.HTTP_200_OK: {'description': 'Swap is OK'},
        status.HTTP_503_SERVICE_UNAVAILABLE: {'description': 'Swap is unavailable'},
    },
)
async def get_is_swap_available():
    res = await SwapService.is_swap_available()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Swap in unavailable',
        )


@router.get(
    '/fee',
    responses={
        status.HTTP_200_OK: {'description': 'Returns swap fee'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'No swap fee'},
    },
)
async def get_swap_fee():
    fee = await AdminService.get_constant(Const.FEE_SWAP)
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'No swap fee'
        )

    return FeeResponse(fee=fee)


@router.post(
    '/add',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add user swap and update user balance'
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user not found'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_swap(data: AddSwapRequest):
    user_wallet = await UserService.get_user_wallet(data.user_id)
    if not user_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found',
        )

    if data.from_token == 'TON':
        to_token_price = await TokenService.get_ton_to_usdt_price()
        if not to_token_price:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Some server error occurred',
            )

        volume = to_token_price * float(data.from_amount)
    elif data.from_token == 'USDT':
        to_token_price = await TokenService.get_usdt_to_ton_price()
        if not to_token_price:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Some server error occurred',
            )

        volume = data.from_amount
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Token {data.from_token.upper()} not found',
        )

    fee = await AdminService.get_constant(Const.FEE_SWAP)
    if not fee or fee > 100 or fee < 0:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Some server error occurred'
        )

    to_amount = float(data.from_amount) * to_token_price
    to_amount -= to_amount * fee / 100

    admin_wallet = await UserService.get_user_wallet(user_id=config.ADMIN_ID)
    if data.from_token == 'TON' and admin_wallet.usdt_balance < to_amount:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Some server error occurred'
        )
    elif data.from_token == 'USDT' and admin_wallet.ton_balance < to_amount:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Some server error occurred'
        )

    await UserService.add_user_swap(
        user_id=data.user_id,
        ton_balance=user_wallet.ton_balance,
        usdt_balance=user_wallet.usdt_balance,
        from_token=data.from_token,
        from_amount=float(data.from_amount),
        to_token=data.to_token,
        to_amount=to_amount,
        volume=float(volume),
    )

    if data.from_token == 'TON':
        await UserService.update_balance(
            user_id=config.ADMIN_ID,
            new_ton_balance=admin_wallet.ton_balance + float(data.from_amount),
            new_usdt_balance=admin_wallet.usdt_balance - to_amount,
        )
    elif data.from_token == 'USDT':
        await UserService.update_balance(
            user_id=config.ADMIN_ID,
            new_ton_balance=admin_wallet.ton_balance - to_amount,
            new_usdt_balance=admin_wallet.usdt_balance + float(data.from_amount),
        )
