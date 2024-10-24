from src.common import config
from src.service.wallet import Wallet


class SwapService:
    @staticmethod
    async def is_swap_available() -> int | None:
        wallet = Wallet(address=config.TON_WALLET_ADDRESS, is_testnet=config.IS_TESTNET)

        balance = await wallet.get_balance()
        if not balance:
            return

        tron_balance = await Wallet.get_tron_balance()
        if not tron_balance:
            return

        return 1
