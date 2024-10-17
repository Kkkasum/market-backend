from fastapi import APIRouter, status, HTTPException

from pytoniq_core import Address, AddressError

from ._schemas import (
    DepositAddressResponse,
    DepositTokenRequest,
    DepositNumberRequest,
    DepositUsernameRequest
)
from src.service.deposit import DepositService

router = APIRouter()


@router.get(
    '/address',
    responses={
        status.HTTP_200_OK: {
            'description': 'Returns address for user deposit'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Deposit address not found'
        }
    }
)
async def get_deposit_address():
    return DepositAddressResponse(
        deposit_address=DepositService.testnet_deposit_address
    )


@router.post(
    '/token',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Deposit user token'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified sender address and/or destination address are/is invalid'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def deposit_token(data: DepositTokenRequest):
    try:
        sender_addr = Address(data.sender)
        deposit_addr = Address(data.destination)
    except AddressError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Sender {data.sender} and/or {data.destination} are/is invalid'
        )

    await DepositService.deposit_ton_toncenter(
        sender_addr=sender_addr,
        deposit_addr=deposit_addr,
        testnet=True
    )


@router.post(
    '/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Deposit user number'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def deposit_number(data: DepositNumberRequest):
    pass


@router.post(
    '/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Deposit user username'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def deposit_username(data: DepositUsernameRequest):
    pass