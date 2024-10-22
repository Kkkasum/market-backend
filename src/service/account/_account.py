import asyncio
from datetime import datetime

from pytoniq_core import Address

from src.service.deposit import DepositService


class AccountSubscription:
    def __init__(self, address: Address, start_time: datetime):
        self.address = address
        self.start_time = start_time

    async def get_transactions(
        self,
        time: datetime,
        offset_transaction_lt: None = None,
        offset_transaction_hash: None = None,
    ) -> None:
        count = 10

        txs = await DepositService.get_wallet_transactions(
            self.address.to_str(), int(self.start_time.timestamp()), testnet=True
        )
        if not txs:
            await asyncio.sleep(5)
            return await self.get_transactions(
                time=time,
                offset_transaction_lt=offset_transaction_lt,
                offset_transaction_hash=offset_transaction_hash
            )

        if not len(txs):
            pass
