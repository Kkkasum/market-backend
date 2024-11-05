from hashlib import md5 as sha256
from math import floor
from time import time

from fastapi import APIRouter, status, HTTPException, Query
from loguru import logger

from src.common import MIN_RUB_DEPOSIT
from src.database import PaymentType
from src.service.admin import AdminService, Const
from src.service.deposit import DepositService
from src.service.history import HistoryService
from src.service.token import TokenService
from src.service.user import UserService
from ._schemas import (
    DepositAddressResponse,
    RequisiteResponse,
    DepositTronRequest,
    DepositRubRequest,
)

router = APIRouter()


@router.get(
    '/crypto/{network}/{user_id}',
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


@router.get(
    '/rub/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': RequisiteResponse,
            'description': 'Returns requisite for specified amount and payment_type',
        },
        status.HTTP_400_BAD_REQUEST: {'description': 'Invalid query params'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {'description': 'Service is unavailable'},
    },
)
async def get_deposit_requisite(
    user_id: int,
    amount: int = Query(),
    payment_type: PaymentType = Query(alias='payment'),
):
    if amount < MIN_RUB_DEPOSIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The minimum rub deposit is {MIN_RUB_DEPOSIT}',
        )

    fee = await AdminService.get_constant(Const.FEE_RUB_DEPOSIT)
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable',
        )

    personal_id = sha256(bytes(f'{user_id}{int(time())}', encoding='utf-8')).hexdigest()

    requisite = await DepositService.get_deposit_rub_requisite(
        amount=amount, payment_type=payment_type.lower(), personal_id=personal_id
    )
    if not requisite:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred',
        )

    await HistoryService.add_rub_deposit(
        user_id, personal_id, requisite.onlypays_id, payment_type
    )

    return RequisiteResponse(
        fee=str(fee),
        requisite=requisite.requisite,
        owner=requisite.owner,
        bank=requisite.bank,
    )


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
    user = await UserService.get_user_wallet(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found'
        )

    tx = await HistoryService.get_deposit_by_tx_hash(tx_hash=data.tx_id)
    if tx:
        return

    if (
        'USDT-TRC20' in data.coin
        and data.status != 'network_error'
        and float(data.amount) >= 10
    ):
        await UserService.add_deposit(
            user_id=user_id,
            ton_balance=user.ton_balance,
            usdt_balance=user.usdt_balance,
            token='USDT',
            amount=float(data.amount),
            tx_hash=data.tx_id,
        )

    logger.success(f'Add {data.amount} as deposit for user {user_id}')


@router.post(
    '/onlypays/rub',
    responses={
        status.HTTP_201_CREATED: {'description': 'Add rub deposit'},
        status.HTTP_404_NOT_FOUND: {'description': 'Specified personal ID not found'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_rub_deposit(data: DepositRubRequest):
    if data.received_sum < MIN_RUB_DEPOSIT:
        return

    fee = await AdminService.get_constant(Const.FEE_RUB_DEPOSIT)
    if not fee:
        return

    rub_deposit = await HistoryService.get_rub_deposit(
        personal_id=data.personal_id, onlypays_id=data.onlypays_id
    )
    if not rub_deposit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Order #{data.onlypays_id} ({data.personal_id}) not found',
        )

    usdt_to_rub_price = await TokenService.get_usdt_to_rub_price()
    if not usdt_to_rub_price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Some server error occurred',
        )

    amount_usdt = data.received_sum * usdt_to_rub_price
    amount_usdt -= amount_usdt * fee / 100
    amount_usdt = floor(amount_usdt * 10**2) / 10**2

    await HistoryService.update_rub_deposit(
        id=rub_deposit.id,
        status='success',
        amount_rub=data.received_sum,
        amount_usdt=amount_usdt,
    )

    user = await UserService.get_user_wallet(user_id=rub_deposit.user_id)
    await UserService.update_usdt_balance(
        user_id=rub_deposit.user_id, new_usdt_balance=user.usdt_balance + amount_usdt
    )
