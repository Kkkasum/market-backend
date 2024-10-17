from fastapi import APIRouter, status, HTTPException
from pytoniq import RunGetMethodError
from pytoniq_core import Address, AddressError

from ._schemas import UsernameResponse, UsernameByAddressResponse
from src.service.username import UsernameService

router = APIRouter()


@router.get(
    '/{un}',
    responses={
        status.HTTP_200_OK: {
            'model': UsernameResponse,
            'description': 'Returns data for specified username'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified username not found'
        }
    }
)
async def get_username(un: str):
    username = await UsernameService.get_username(un)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Username {un} not found'
        )

    return UsernameResponse.model_validate(username, from_attributes=True)


@router.get(
    '/contract/{address}',
    responses={
        status.HTTP_200_OK: {
            'model': UsernameByAddressResponse,
            'description': 'Returns username for specified username contract address'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified address is invalid'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified contract is not teleitem'
        }
    }
)
async def get_username_by_address(address: str):
    try:
        address = Address(address)
    except AddressError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Address {address} is invalid'
        )

    try:
        username = await UsernameService.get_username_by_address(address)
    except RunGetMethodError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Contract {address} is not teleitem'
        )

    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Contract {address} is not teleitem'
        )

    return UsernameByAddressResponse(
        username=username
    )