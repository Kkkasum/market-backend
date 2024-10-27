from src.common import config, r
from src.service.user import UserService


class SwapService:
    @staticmethod
    async def is_swap_available() -> int | None:
        res = await r.get('is_swap_available')
        if res and int(res):
            return 1

        user = await UserService.get_user_wallet(user_id=config.ADMIN_ID)

        if not user.ton_balance:
            await r.setex(name='is_swap_available', value=0, time=10)
            return

        if not user.usdt_balance:
            await r.setex(name='is_swap_available', value=0, time=10)
            return

        return 1
