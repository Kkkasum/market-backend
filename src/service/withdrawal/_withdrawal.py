import aiohttp

from tonutils.wallet import HighloadWalletV3
from tonutils.client import TonapiClient

from src.common import config


class WithdrawalService:
    @staticmethod
    async def withdraw_usdt(address: str, amount: float) -> str | None:
        url = 'https://b2bwallet.io/api/v1/withdrawal'
        headers = {
            'Content-Type': 'application/json'
        }
        json = {
            'coin': 'USDT-TRC20',
            'amount': f'{amount:.2f}',
            'address': address
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res['id']

    @staticmethod
    async def withdraw_ton(user_id: int, destination: str, amount: float) -> int | None:
        client = TonapiClient(api_key=config.TONAPI_KEY, is_testnet=True)
        mnemonics = config.MNEMONICS.split(' ')

        wallet, _, _, _ = HighloadWalletV3.from_mnemonic(client, mnemonics, wallet_id=239, timeout=128)

        balance = await client.get_account_balance(wallet.address.to_str()) / 10 ** 9
        if balance < 0.1:
            return 1

        print(f'Withdraw for user {user_id}, destination: {destination}, amount: {amount}')
        await wallet.transfer(destination=destination, amount=amount)

    @staticmethod
    async def withdraw_nft(user_id: int, destination: str, nft_address: str) -> int | None:
        client = TonapiClient(api_key=config.TONAPI_KEY, is_testnet=True)
        mnemonics = config.MNEMONICS.split(' ')

        wallet, _, _, _ = HighloadWalletV3.from_mnemonic(client, mnemonics, wallet_id=239, timeout=128)

        balance = await client.get_account_balance(wallet.address.to_str()) / 10 ** 9
        if balance < 0.1:
            return 1

        print(f'Withdraw for user {user_id}, destination: {destination}, nft_address: {nft_address}')
        await wallet.transfer_nft(destination=destination, nft_address=nft_address)
