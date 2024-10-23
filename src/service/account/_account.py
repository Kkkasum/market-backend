import aiohttp
from pytoniq_core import Cell, Address, AddressError

from ._models import Message, NftTransfer
from src.service.history import HistoryService
from src.service.user import UserService
from src.service.number import NumberService
from src.service.username import UsernameService
from src.common import config, MIN_TON_DEPOSIT, NUMBERS_COLLECTION_ADDRESS, USERNAMES_COLLECTION_ADDRESS


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

    async def get_wallet_nft_transfers(self, collection_address: str) -> list[dict] | None:
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
            'start_utime': self.start_utime,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                return res['nft_transfers']

    async def get_nft_transfers(self, collection_address: str) -> list[NftTransfer] | None:
        nft_transfers = await self.get_wallet_nft_transfers(collection_address)
        if not nft_transfers:
            return

        if not len(nft_transfers):
            return

        if int(nft_transfers[-1]['created_at']) < self.start_utime:
            return

        return [
            NftTransfer.model_validate(nft_transfer, from_attributes=True)
            for nft_transfer in nft_transfers
        ]

    @staticmethod
    async def get_number_nft_transfer_data(nft_transfer: NftTransfer) -> [int, str, str]:
        try:
            nft_address = Address(nft_transfer.nft_address)
        except AddressError:
            return

        number = await NumberService.get_number_by_address(nft_address)
        if not number:
            return

        comment = Cell.one_from_boc(nft_transfer.forward_payload).begin_parse().skip_bits(32)
        user_id = comment.load_string()

        return [user_id, number, nft_address.to_str()]

    @staticmethod
    async def get_username_nft_transfer_data(nft_transfer: NftTransfer) -> [int, str, str]:
        try:
            nft_address = Address(nft_transfer.nft_address)
        except AddressError:
            return

        username = await UsernameService.get_username_by_address(nft_address)
        if not username:
            return

        comment = Cell.one_from_boc(nft_transfer.forward_payload).begin_parse().skip_bits(32)
        user_id = comment.load_string()

        return user_id, username, nft_address.to_str()

    async def check_for_numbers_transfers(self) -> None:
        transfers = await self.get_nft_transfers(NUMBERS_COLLECTION_ADDRESS)
        if not transfers:
            return

        for transfer in transfers:
            nft_transfer_data = await self.get_number_nft_transfer_data(transfer)
            if nft_transfer_data:
                user_id, number, address = nft_transfer_data

                user = await UserService.get_user(user_id)
                if not user:
                    return

                number_id = await NumberService.add_number(number, address)
                await UserService.add_user_number(user_id, number_id)

    async def check_for_usernames_transfers(self) -> None:
        transfers = await self.get_nft_transfers(USERNAMES_COLLECTION_ADDRESS)
        if not transfers:
            return

        for transfer in transfers:
            nft_transfer_data = await self.get_username_nft_transfer_data(transfer)
            if nft_transfer_data:
                user_id, username, address = nft_transfer_data

                user = await UserService.get_user(user_id)
                if not user:
                    return

                username_id = await UsernameService.add_username(username, address)
                await UserService.add_user_username(user_id, username_id)
