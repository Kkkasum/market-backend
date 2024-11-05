import aiohttp
from pytoniq_core import Address

from src.common import config
from ._models import Requisite


class DepositService:
    @staticmethod
    async def get_deposit_ton_address(testnet: bool = False) -> str:
        deposit_address = Address(config.TON_WALLET_ADDRESS).to_str(
            is_test_only=testnet
        )

        return deposit_address

    @staticmethod
    async def get_deposit_tron_address(user_id: int) -> str | None:
        url = 'https://b2bwallet.io/api/v1/address'
        headers = {'X-Api-Key': config.B2B_API_KEY, 'Content-Type': 'application/json'}
        json = {
            'coin': 'USDT-TRC20',
            'callback_url': f'https://useton.net/api/deposit/tron/{user_id}',
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json, headers=headers) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res['address']

    @staticmethod
    async def get_deposit_rub_requisite(
        amount: int, payment_type: str, personal_id: str
    ) -> Requisite | None:
        url = 'https://onlypays.org/get_requisite'
        json = {
            'api_id': config.ONLYPAYS_API_ID,
            'secret_key': config.ONLYPAYS_SECRET_KEY,
            'amount_rub': amount,
            'payment_type': payment_type,
            'personal_id': personal_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                is_success = res['success']
                if not is_success:
                    return

                return Requisite.model_validate(res['data'], from_attributes=True)
