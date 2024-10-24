from fastapi import APIRouter

from src.api.user import router as user_router
from src.api.deposit import router as deposit_router
from src.api.withdrawal import router as withdrawal_router
from src.api.swap import router as swap_router
from src.api.number import router as number_router
from src.api.username import router as username_router
from src.api.token import router as token_router
from src.api.market import router as market_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(deposit_router, prefix='/deposit', tags=['Deposit'])
router.include_router(withdrawal_router, prefix='/withdrawal', tags=['Withdrawal'])
router.include_router(swap_router, prefix='/swap', tags=['Swap'])
router.include_router(number_router, prefix='/number', tags=['Number'])
router.include_router(username_router, prefix='/username', tags=['Username'])
router.include_router(token_router, prefix='/token', tags=['Token'])
router.include_router(market_router, prefix='/market', tags=['Market'])
