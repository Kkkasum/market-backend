from fastapi import APIRouter, status, HTTPException

from ._schemas import TokenRateResponse
from src.service.token import TokenService

router = APIRouter()


@router.get(
    '/rate/{token}',
    responses={
        status.HTTP_200_OK: {
            'model': TokenRateResponse,
            'description': 'Returns price for specified token from CMC'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified token not found'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Some server error occurred'
        }
    }
)
async def get_token_rate(token: str):
    if token == 'TON':
        token_price = await TokenService.get_ton_to_usdt_price()
    elif token == 'USDT':
        token_price = await TokenService.get_usdt_to_ton_price()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Token {token.upper()} not found'
        )

    if not token_price:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Could not get token price'
        )

    return TokenRateResponse(
        token=token,
        rate=f'{token_price}'
    )
