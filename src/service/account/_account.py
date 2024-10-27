from pytoniq_core import Cell, Address, AddressError

from src.common import (
    MIN_TON_DEPOSIT,
    NUMBERS_COLLECTION_ADDRESS,
    USERNAMES_COLLECTION_ADDRESS,
)
from src.service.history import HistoryService
from src.service.number import NumberService
from src.service.user import UserService
from src.service.username import UsernameService
from src.service.wallet import Wallet, Message, NftTransfer


class AccountSubscription:
    def __init__(self, wallet: Wallet, start_utime: int):
        self.wallet = wallet
        self.start_utime = start_utime

    @staticmethod
    async def validate_deposit_message(msg: Message) -> bool | None:
        if not msg.source:
            # external message
            return

        if not msg.value or float(msg.value) / 10**9 < MIN_TON_DEPOSIT:
            # check msg value
            return

        res = await HistoryService.get_deposit_by_tx_hash(tx_hash=msg.hash)
        if res:
            # tx is already checked
            return

        if (
            not msg.message_content
            or not msg.message_content.decoded
            or not msg.message_content.decoded.comment
        ):
            return

        return True

    @staticmethod
    async def validate_nft_transfer(
        nft_transfer: NftTransfer, is_number: bool = False
    ) -> tuple[int, str, str] | None:
        try:
            nft_address = Address(nft_transfer.nft_address)
        except AddressError:
            return

        if is_number:
            asset = await NumberService.get_number_by_address(nft_address)
        else:
            asset = await UsernameService.get_username_by_address(nft_address)

        if not asset:
            return

        comment = (
            Cell.one_from_boc(nft_transfer.forward_payload).begin_parse().skip_bits(32)
        )

        try:
            user_id = int(comment.load_string())
        except ValueError:
            return

        return user_id, asset, nft_address.to_str()

    async def check_for_deposit(self) -> None:
        messages = await self.wallet.get_messages(self.start_utime)
        if not messages:
            return

        for message in messages:
            res = await self.validate_deposit_message(message)
            if res:
                tx_hash, user_id, ton_deposit = (
                    message.hash,
                    int(message.message_content.decoded.comment),
                    float(message.value) / 10**9,
                )

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

    async def check_for_numbers_transfers(self) -> None:
        transfers = await self.wallet.get_nft_transfers(
            NUMBERS_COLLECTION_ADDRESS, self.start_utime
        )
        if not transfers:
            return

        for transfer in transfers:
            nft_transfer_data = await self.validate_nft_transfer(
                transfer, is_number=True
            )
            if nft_transfer_data:
                user_id, number, address = nft_transfer_data

                user = await UserService.get_user_wallet(user_id)
                if not user:
                    return

                number_id = await NumberService.add_number(number, address)
                await UserService.add_user_number(user_id, number_id)

    async def check_for_usernames_transfers(self) -> None:
        transfers = await self.wallet.get_nft_transfers(
            USERNAMES_COLLECTION_ADDRESS, self.start_utime
        )
        if not transfers:
            return

        for transfer in transfers:
            nft_transfer_data = await self.validate_nft_transfer(transfer)
            if nft_transfer_data:
                user_id, username, address = nft_transfer_data

                user = await UserService.get_user_wallet(user_id)
                if not user:
                    return

                username_id = await UsernameService.add_username(username, address)
                await UserService.add_user_username(user_id, username_id)
