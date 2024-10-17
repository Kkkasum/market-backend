from fastapi import APIRouter, status, HTTPException

from ._schemas import WithdrawTokenRequest, WithdrawNumberRequest, WithdrawUsernameRequest

router = APIRouter()


@router.post(
    '/token',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw user token'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_token(data: WithdrawTokenRequest):
    pass


@router.post(
    '/number',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw user number'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_number(data: WithdrawNumberRequest):
    pass


@router.post(
    '/username',
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Withdraw user username'
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Specified user not found'
        }
    },
    status_code=status.HTTP_201_CREATED
)
async def withdraw_username(data: WithdrawUsernameRequest):
    pass