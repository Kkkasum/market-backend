import asyncio
import aiohttp

from ._models import Message
from src.service.history import HistoryService
from src.service.user import UserService
from src.common import config, MIN_TON_DEPOSIT


class AccountSubscription:
    def __init__(self, address: str, start_utime: int, is_testnet: bool = True):
        self.address = address
        self.start_utime = start_utime
        self.is_testnet = is_testnet

    async def get_wallet_messages(self) -> list[dict] | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if self.is_testnet
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/messages'
        headers = {
            'X-Api-Key': config.TONCENTER_API_KEY_TESTNET if self.is_testnet else config.TONCENTER_API_KEY
        }
        params = {
            'destination': self.address,
            'start_utime': self.start_utime,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                print(res)

                return res['messages']

    async def get_messages(self) -> list[Message] | None:
        msgs = await self.get_wallet_messages()
        if not msgs:
            return

        if not len(msgs):
            return

        if int(msgs[-1]['created_at']) < self.start_utime:
            return

        return [
            Message.model_validate(msg, from_attributes=True)
            for msg in msgs
        ]

    @staticmethod
    async def get_deposit_data(msg: Message) -> [str, int, float]:
        msg = Message.model_validate(msg, from_attributes=True)
        if not msg.source:
            # external message
            return

        if not msg.value or float(msg.value) / 10 ** 9 < MIN_TON_DEPOSIT:
            # check msg value
            return

        res = await HistoryService.get_deposit_by_tx_hash(tx_hash=msg.hash)
        if res:
            # tx is already checked
            return

        if not msg.message_content or not msg.message_content.decoded or not msg.message_content.decoded.comment:
            return

        return [msg.hash, int(msg.message_content.decoded.comment), float(msg.value) / 10 ** 9]

    async def check_for_deposit(self) -> None:
        msgs = await self.get_messages()
        if not msgs:
            return

        for msg in msgs:
            deposit_data = await self.get_deposit_data(msg)
            if deposit_data:
                tx_hash, user_id, ton_deposit = deposit_data
                user = await UserService.get_user(user_id)
                if not user:
                    continue

                await UserService.add_deposit(
                    user_id=user_id,
                    ton_balance=user.ton_balance,
                    usdt_balance=user.usdt_balance,
                    token='TON',
                    amount=ton_deposit,
                    tx_hash=tx_hash,
                )
