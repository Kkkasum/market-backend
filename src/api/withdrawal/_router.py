from fastapi import APIRouter, status, HTTPException

from ._schemas import WithdrawUsdtRequest, WithdrawTonRequest, WithdrawNumberRequest, WithdrawUsernameRequest
from src.service.withdrawal import WithdrawalService
from src.service.user import UserService
from src.service.number import NumberService, Status as NumberStatus
from src.service.username import UsernameService, Status as UsernameStatus

router = APIRouter()


@router.post(
    '/usdt',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw USDT-TRC20 to specified address for specified user'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has not enough balance'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            'description': 'Invalid TRON address'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_usdt(data: WithdrawUsdtRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    if user.usdt_balance < data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has not enough balance'
        )

    res = await WithdrawalService.withdraw_usdt(data.address, data.amount)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Some server error occurred'
        )

    await UserService.add_withdrawal(
        user_id=user.user_id,
        ton_balance=user.ton_balance,
        usdt_balance=user.usdt_balance,
        token='USDT',
        amount=data.amount,
        address=data.address,
        tx_hash=res,
    )


@router.post(
    '/ton',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw TON-TON to specified address for specified user'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified user has not enough balance'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_ton(data: WithdrawTonRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    if user.ton_balance < data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User {data.user_id} has not enough balance'
        )

    await WithdrawalService.withdraw_ton(data.user_id, data.address, data.amount)

    await UserService.add_withdrawal(
        user_id=user.user_id,
        ton_balance=user.ton_balance,
        usdt_balance=user.usdt_balance,
        token='TON',
        amount=data.amount,
        address=data.address,
        tx_hash='123',
    )


@router.post(
    '/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw user token'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified number not found'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified user has not specified number'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_number(data: WithdrawNumberRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    number = await NumberService.get_number(data.number)
    if not number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Number {data.number} not found'
        )

    if number.owner_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'User {data.user_id} has not number {data.number}'
        )

    await NumberService.delete_number(data.number)
    await WithdrawalService.withdraw_nft(data.user_id, data.address, number.address)


@router.post(
    '/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw user token'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified username not found'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
        status.HTTP_405_METHOD_NOT_ALLOWED: {
            'description': 'Specified user has not specified username'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_username(data: WithdrawUsernameRequest):
    user = await UserService.get_user_wallet(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {data.user_id} not found'
        )

    username = await UsernameService.get_username(data.username)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Username {data.username} not found'
        )

    if username.owner_id != data.user_id:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f'User {data.user_id} has not username {data.username}'
        )

    await UsernameService.delete_username(data.username)
    await WithdrawalService.withdraw_nft(data.user_id, data.address, username.address)