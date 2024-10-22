from fastapi import APIRouter, status, HTTPException

from loguru import logger

from ._schemas import (
    DepositAddressResponse,
    DepositTronRequest,
    DepositTonRequest,
)
from src.common import config, MIN_TON_DEPOSIT
from src.service.deposit import DepositService
from src.service.user import UserService
from src.service.history import HistoryService

router = APIRouter()


@router.post(
    '/tron/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'description': 'Add tron deposit'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Service is unavailable'
        }
    }
)
async def add_tron_deposit(user_id: int, data: DepositTronRequest):
    user = await UserService.get_user_wallet(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {user_id} not found'
        )

    if 'USDT' in data.coin and data.status == 'confirmed':
        await UserService.add_deposit(
            user_id=user_id,
            ton_balance=user.ton_balance,
            usdt_balance=user.usdt_balance,
            token=data.token,
            amount=float(data.amount),
            tx_hash=data.tx_hash,
        )


@router.post(
    '/ton',
    responses={
        status.HTTP_200_OK: {
            'description': 'Add ton deposit'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Deposit value is less than min ton deposit'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    }
)
async def add_ton_deposit(data: DepositTonRequest):
    logger.success(data)
    try:
        res = await HistoryService.get_deposit_by_tx_hash(data.tx_hash)
        if res:
            return

        tx = await DepositService.get_wallet_transaction(data.tx_hash)
        if not tx:
            return

        msg = tx['in_msg']
        if msg['destination'] != config.TON_WALLET_ADDRESS:
            return

        user_id = msg['message_content']['decoded']['comment']
        user = await UserService.get_user_wallet(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User {user_id} not found'
            )

        ton_deposit = msg['value'] / 10 ** 9
        if ton_deposit < MIN_TON_DEPOSIT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Deposit value {ton_deposit} is less than min ton deposit'
            )

        await UserService.add_deposit(
            user_id=user.user_id,
            ton_balance=user.ton_balance,
            usdt_balance=user.usdt_balance,
            token='TON',
            amount=ton_deposit,
            tx_hash=data.tx_hash,
        )
    except Exception as e:
        logger.error(e)


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
    }
)
async def get_deposit_address(network: str, user_id: int):
    if network == 'TRON':
        deposit_address = await UserService.get_user_tron_address(user_id)
        if deposit_address:
            return DepositAddressResponse(
                deposit_address=deposit_address
            )

        deposit_address = await DepositService.get_deposit_usdt_address(user_id)
        if not deposit_address:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f'Deposit address is unavailable for network {network}'
            )

        await UserService.add_user_tron_address(user_id, deposit_address)

        return DepositAddressResponse(
            deposit_address=deposit_address
        )

    if network == 'TON':
        deposit_address = await DepositService.get_deposit_ton_address()
        if not deposit_address:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f'Deposit address is unavailable for network {network}'
            )
        return DepositAddressResponse(
            deposit_address=deposit_address
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'No deposit address for network {network}'
    )
