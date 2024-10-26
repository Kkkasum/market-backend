import aiohttp
from loguru import logger
from pytoniq_core import begin_cell
from tonutils.client import TonapiClient
from tonutils.wallet import HighloadWalletV3

from src.common import config


class WithdrawalService:
    @staticmethod
    async def withdraw_usdt(address: str, amount: float) -> str | None:
        url = 'https://b2bwallet.io/api/v1/withdrawal'
        headers = {'Content-Type': 'application/json'}
        json = {'coin': 'USDT-TRC20', 'amount': f'{amount:.2f}', 'address': address}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res['id']

    @staticmethod
    async def withdraw_ton(
        user_id: int, destination: str, tag: str | None, amount: float
    ) -> int | str:
        client = TonapiClient(api_key=config.TONAPI_KEY, is_testnet=config.IS_TESTNET)
        mnemonics = config.MNEMONICS.split(' ')

        wallet, _, _, _ = HighloadWalletV3.from_mnemonic(
            client, mnemonics, wallet_id=239
        )

        balance = await client.get_account_balance(wallet.address.to_str()) / 10**9
        if balance < 0.1 or balance < amount:
            return 1

        logger.success(
            f'Withdraw for user {user_id}, destination: {destination}, amount: {amount}'
        )
        message_hash = await wallet.transfer(
            destination=destination,
            amount=amount,
            body=begin_cell()
            .store_uint(0, 32)
            .store_string(str(tag or user_id))
            .end_cell(),
        )

        return message_hash

    @staticmethod
    async def withdraw_nft(
        user_id: int, destination: str, nft_address: str
    ) -> int | str:
        client = TonapiClient(api_key=config.TONAPI_KEY, is_testnet=config.IS_TESTNET)
        mnemonics = config.MNEMONICS.split(' ')

        wallet, _, _, _ = HighloadWalletV3.from_mnemonic(
            client, mnemonics, wallet_id=239
        )

        balance = await client.get_account_balance(wallet.address.to_str()) / 10**9
        if balance < 0.1:
            return 1

        logger.success(
            f'Withdraw NFT for user {user_id}, destination: {destination}, nft_address: {nft_address}'
        )
        message_hash = await wallet.transfer_nft(
            destination=destination, nft_address=nft_address
        )

        return message_hash
