from fastapi import APIRouter, status, HTTPException

from src.service.deposit import DepositService
from src.service.user import UserService
from ._schemas import (
    DepositAddressResponse,
    DepositTronRequest,
)

router = APIRouter()


@router.post(
    '/tron/{user_id}',
    responses={
        status.HTTP_200_OK: {'description': 'Add tron deposit'},
        status.HTTP_404_NOT_FOUND: {'description': 'Specified user not found'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Service is unavailable'
        },
    },
)
async def add_tron_deposit(user_id: int, data: DepositTronRequest):
    print(data.coin)
    user = await UserService.get_user_wallet(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found'
        )

    if 'USDT-TRC20' in data.coin and data.status != 'network_error':
        await UserService.add_deposit(
            user_id=user_id,
            ton_balance=user.ton_balance,
            usdt_balance=user.usdt_balance,
            token=data.token,
            amount=float(data.amount),
            tx_hash=data.tx_hash,
        )


@router.get(
    '/{network}/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'description': 'Returns deposit address for specified network'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'No deposit address for specified network'
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            'description': 'Deposit address is unavailable for specified network'
        },
    },
)
async def get_deposit_address(network: str, user_id: int):
    if network == 'TRON':
        deposit_address = await UserService.get_user_tron_address(user_id)
        if deposit_address:
            return DepositAddressResponse(deposit_address=deposit_address)

        deposit_address = await DepositService.get_deposit_tron_address(user_id)
        if not deposit_address:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f'Deposit address is unavailable for network {network}',
            )

        await UserService.add_user_tron_address(user_id, deposit_address)

        return DepositAddressResponse(deposit_address=deposit_address)

    if network == 'TON':
        deposit_address = await DepositService.get_deposit_ton_address()
        if not deposit_address:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f'Deposit address is unavailable for network {network}',
            )
        return DepositAddressResponse(deposit_address=deposit_address)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'No deposit address for network {network}',
    )
