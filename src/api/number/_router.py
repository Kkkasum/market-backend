from fastapi import APIRouter, status, HTTPException

from pytoniq import RunGetMethodError
from pytoniq_core import Address, AddressError

from ._schemas import NumberResponse, NumberByAddressResponse
from src.service.number import NumberService

router = APIRouter()


@router.get(
    '/{n}',
    responses={
        status.HTTP_200_OK: {
            'model': NumberResponse,
            'description': 'Returns data for specified number'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified number not found'
        }
    }
)
async def get_number(n: str):
    number = await NumberService.get_number(n)
    if not number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Number {n} not found'
        )

    return NumberResponse.model_validate(number, from_attributes=True)


@router.get(
    '/contract/{address}',
    responses={
        status.HTTP_200_OK: {
            'model': NumberByAddressResponse,
            'description': 'Returns number for specified number contract address'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Specified address is invalid'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified contract is not teleitem'
        }
    }
)
async def get_number_by_address(address: str):
    try:
        address = Address(address)
    except AddressError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Address {address} is invalid'
        )

    try:
        number = await NumberService.get_number_by_address(address)
    except RunGetMethodError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Contract {address} is not teleitem'
        )

    if not number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Contract {address} is not teleitem'
        )

    return NumberByAddressResponse(
        number=number
    )
