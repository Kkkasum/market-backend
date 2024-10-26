from src.common import config, r
from src.service.wallet import Wallet


class SwapService:
    @staticmethod
    async def is_swap_available() -> int | None:
        res = await r.get('is_swap_available')
        if res and int(res):
            return 1

        wallet = Wallet(address=config.TON_WALLET_ADDRESS, is_testnet=config.IS_TESTNET)

        balance = await wallet.get_balance()
        if not balance:
            await r.setex(name='is_swap_available', value=0, time=10)
            return

        tron_balance = await Wallet.get_tron_balance()
        if not tron_balance:
            await r.setex(name='is_swap_available', value=0, time=10)
            return

        return 1
