import aiohttp

from pytoniq_core import Address

from src.common import config


class DepositService:
    @staticmethod
    async def get_deposit_ton_address(testnet: bool = False) -> str:
        deposit_address = Address(config.TON_WALLET_ADDRESS).to_str(is_test_only=testnet)

        return deposit_address

    @staticmethod
    async def get_deposit_usdt_address(user_id: int) -> str | None:
        url = 'https://b2bwallet.io/api/v1/address'
        headers = {
            'X-Api-Key': config.B2B_API_KEY,
            'Content-Type': 'application/json'
        }
        json = {
            'coin': 'USDT-TRC20',
            'callback_url': 'https://useton.net/'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json, headers=headers) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res['address']

    @staticmethod
    async def get_wallet_transaction(tx_hash: str, testnet: bool = True) -> dict | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if testnet
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/transactions'
        headers = {
            'X-Api-Key': config.TONCENTER_API_KEY_TESTNET if testnet else config.TONCENTER_API_KEY
        }
        params = {
            'hash': tx_hash
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res

    @staticmethod
    async def deposit_ton_toncenter(sender_addr: Address, deposit_addr: Address, testnet: bool = True):
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if testnet
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/messages'
        headers = {
            'X-Api-Key': config.TONCENTER_API_KEY_TESTNET if testnet else config.TONCENTER_API_KEY
        }
        params = {
            'source': sender_addr.to_str(),
            'destination': deposit_addr.to_str(),
            'direction': 'out'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                print(res['messages'][0])
