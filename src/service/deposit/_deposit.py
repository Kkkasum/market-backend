import aiohttp

from pytoniq import LiteClient, LiteBalancer
from pytoniq_core import Address

from ._utils import filter_ton_deposit


class DepositService:
    deposit_address: str = Address('UQAvR5PPWDccqQ6Zu_UlRizMlFfqa7IMK_5TuRwrEySihbVH').to_str()
    testnet_deposit_address: str = (
        Address('UQAvR5PPWDccqQ6Zu_UlRizMlFfqa7IMK_5TuRwrEySihbVH').to_str(is_test_only=True)
    )

    @staticmethod
    async def deposit_ton_toncenter(sender_addr: Address, deposit_addr: Address, testnet: bool = True):
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if testnet
            else 'https://toncenter.com/api/v3'
        )
        api_key = (
            '6236b29d1a4ee988ba06a1becae204628907bf74abeaeea41230a0010506f091'
            if testnet
            else '230247070698f3a372a9b7247d609ba1a6fcda8ce8daa4e79ab8184bb425d44a'
        )

        url = base_url + '/messages'
        headers = {
            'X-Api-Key': api_key
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

    @staticmethod
    async def deposit_ton(sender_addr: Address, deposit_addr: Address, testnet: bool = True):
        client = (
            LiteClient.from_testnet_config(ls_i=1, trust_level=2)
            if testnet
            else LiteClient.from_mainnet_config(ls_i=1, trust_level=2)
        )

        await client.connect()

        last_block = await client.get_trusted_last_mc_block()
        _account, shard_account = await client.raw_get_account_state(deposit_addr, last_block)
        assert shard_account

        last_tx_lt, last_tx_hash = (
            shard_account.last_trans_lt,
            shard_account.last_trans_hash,
        )

        while True:
            print(f'Waiting for {last_block=}')

            txs = await client.get_transactions(
                deposit_addr, 64, last_tx_lt, last_tx_hash
            )
            ton_deps = [tx for tx in txs if filter_ton_deposit(tx)]
            print(f'Got {len(txs)=} with {len(ton_deps)}')

            for tx_dep in ton_deps:
                print(tx_dep.account_addr)
                print(tx_dep.account_addr_hex)
                print(tx_dep.cell.hash.hex())

            last_tx_lt = txs[0].lt
            last_tx_hash = txs[0].cell.hash