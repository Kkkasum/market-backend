import aiohttp

from ._models import Message, NftTransfer
from src.common import config, r


class Wallet:
    def __init__(self, address: str, is_testnet: bool = False):
        self.address = address
        self.is_testnet = is_testnet

    @staticmethod
    async def get_tron_balance() -> float | None:
        balance = await r.get('tron_balance')
        if balance:
            return float(balance)

        url = 'https://b2bwallet.io/api/v1/balance'
        headers = {
            'X-Api-Key': config.B2B_API_KEY,
            'Content-Type': 'application/json'
        }
        json = {
            'coin': 'USDT-TRC20',
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, json=json) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                try:
                    balance = float(res['balance'])
                except ValueError:
                    return

                await r.set(name='tron_balance', value=balance, time=120)

                return balance

    async def get_balance(self) -> float | None:
        balance = await r.get('balance')
        if balance:
            return float(balance)

        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if self.is_testnet
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/accountStates'
        headers = {
            'X-Api-Key': config.TONCENTER_API_KEY_TESTNET if self.is_testnet else config.TONCENTER_API_KEY
        }
        params = {
            'address': self.address,
            'include_boc': 'false'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                try:
                    balance = int(res['accounts'][0]['balance']) / 10 ** 9
                except ValueError:
                    return
                except IndexError:
                    return

                await r.setex(name='balance', value=balance, time=120)

                return balance

    async def get_messages(self, start_utime: int) -> list[Message] | None:
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
            'start_utime': start_utime,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                messages = res['messages']
                if not messages:
                    return

                if not len(messages):
                    return

                if int(messages[-1]['created_at']) < start_utime:
                    return

                return [
                    Message.model_validate(message, from_attributes=True)
                    for message in messages
                ]

    async def get_nft_transfers(self, collection_address: str, start_utime: int) -> list[NftTransfer] | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if self.is_testnet
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/nft/transfers'
        headers = {
            'X-Api-Key': config.TONCENTER_API_KEY_TESTNET if self.is_testnet else config.TONCENTER_API_KEY
        }
        params = {
            'owner_address': self.address,
            'collection_address': collection_address,
            'start_utime': start_utime,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                nft_transfers = res['nft_transfers']
                if not nft_transfers:
                    return

                if not len(nft_transfers):
                    return

                if int(nft_transfers[-1]['created_at']) < start_utime:
                    return

                return [
                    NftTransfer.model_validate(nft_transfer, from_attributes=True)
                    for nft_transfer in nft_transfers
                ]
