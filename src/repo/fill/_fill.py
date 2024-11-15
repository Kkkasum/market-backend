from src.database import (
    new_session,
    User,
    Number,
    Username,
    UserNumber,
    UserUsername,
    UserDeposit,
    UserWithdrawal,
    UserSwap,
    TransactionToken,
    Const,
    Constant,
    UserNftDeposit,
    UserNftWithdrawal,
    MarketOrder,
    MarketAction,
)


class Fill:
    @staticmethod
    async def add_user():
        async with new_session() as session:
            rows = [
                User(id=6640542382, ton_balance=10, usdt_balance=10),
                User(id=1, ton_balance=10, usdt_balance=10),
                User(id=2, ton_balance=10, usdt_balance=10),
                User(id=3, ton_balance=10, usdt_balance=10),
                User(id=4, ton_balance=10, usdt_balance=10),
                User(id=5, ton_balance=10, usdt_balance=10),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_number():
        async with new_session() as session:
            rows = [
                Number(
                    number='88802726984',
                    address='EQCu7UaREKnpfwzYBzUs6Aow7aQMz1c1DCPl5fWfE1OTMkuh',
                ),
                Number(
                    number='88801492756',
                    address='EQBpQfRdYttzL1Zr66_30IH6wgbdauEZud9qwC_yAnz6iroR',
                ),
                Number(
                    number='88805219484',
                    address='EQDDk5BCLgy_gVNIevb6ii42AL2gBJz50XWG2deDQtofNen0',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_username():
        async with new_session() as session:
            rows = [
                Username(
                    username='buildyourgame',
                    address='EQB3IRxNI4UiGnORk0eSHYz9D6xsfoWzQZoqnseXdVzU3PYg',
                ),
                Username(
                    username='kidswallet',
                    address='EQBqg8_bpc3gVzrerc3gjonZOwXmDYW0jS4WgOdSjORsOAh_',
                ),
                Username(
                    username='marketapp',
                    address='EQDJismPyf-MZQBoLWJDBAwIe1vysqXs9q8T_5xpZKJHv4Uw',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_number():
        async with new_session() as session:
            rows = [
                UserNumber(
                    user_id=6640542382,
                    number_id=1,
                ),
                UserNumber(
                    user_id=6640542382,
                    number_id=2,
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_username():
        async with new_session() as session:
            rows = [
                UserUsername(
                    user_id=6640542382,
                    username_id=1,
                ),
                UserUsername(
                    user_id=6640542382,
                    username_id=2,
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_deposits():
        async with new_session() as session:
            rows = [
                UserDeposit(
                    user_id=6640542382,
                    token=TransactionToken.TON,
                    amount=10,
                    tx_hash='1',
                ),
                UserDeposit(
                    user_id=6640542382,
                    token=TransactionToken.USDT,
                    amount=10,
                    tx_hash='2',
                ),
                UserDeposit(
                    user_id=6640542382,
                    token=TransactionToken.USDT,
                    amount=10,
                    tx_hash='3',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_withdrawals():
        async with new_session() as session:
            rows = [
                UserWithdrawal(
                    user_id=6640542382,
                    token=TransactionToken.TON,
                    amount=10,
                    address='UQAvR5PPWDccqQ6Zu_UlRizMlFfqa7IMK_5TuRwrEySihbVH',
                    tx_hash='1',
                ),
                UserWithdrawal(
                    user_id=6640542382,
                    token=TransactionToken.USDT,
                    amount=10,
                    address='UQAvR5PPWDccqQ6Zu_UlRizMlFfqa7IMK_5TuRwrEySihbVH',
                    tx_hash='2',
                ),
                UserWithdrawal(
                    user_id=6640542382,
                    token=TransactionToken.USDT,
                    amount=10,
                    address='UQAvR5PPWDccqQ6Zu_UlRizMlFfqa7IMK_5TuRwrEySihbVH',
                    tx_hash='3',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_swaps():
        async with new_session() as session:
            rows = [
                UserSwap(
                    user_id=6640542382,
                    from_token='TON',
                    from_amount=10,
                    to_token='USDT',
                    to_amount=55,
                    volume=55,
                ),
                UserSwap(
                    user_id=6640542382,
                    from_token='USDT',
                    from_amount=55,
                    to_token='TON',
                    to_amount=10,
                    volume=55,
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_const():
        async with new_session() as session:
            rows = [
                Constant(const=Const.INSTANT_SELL_PERC, value=10),
                Constant(const=Const.MAX_INSTANT_SELL, value=100),
                Constant(const=Const.FEE_WITHDRAWAL_TRON, value=1),
                Constant(const=Const.FEE_WITHDRAWAL_TON, value=1),
                Constant(const=Const.FEE_SWAP, value=1),
                Constant(const=Const.FEE_BUY, value=1),
                Constant(const=Const.FEE_SELL, value=1),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_nft_deposits():
        async with new_session() as session:
            rows = [
                UserNftDeposit(
                    user_id=6640542382,
                    nft_name='88802726984',
                    nft_address='EQCu7UaREKnpfwzYBzUs6Aow7aQMz1c1DCPl5fWfE1OTMkuh',
                    tx_hash='1',
                ),
                UserNftDeposit(
                    user_id=6640542382,
                    nft_name='buildyourgame',
                    nft_address='EQB3IRxNI4UiGnORk0eSHYz9D6xsfoWzQZoqnseXdVzU3PYg',
                    tx_hash='2',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_nft_withdrawals():
        async with new_session() as session:
            rows = [
                UserNftWithdrawal(
                    user_id=6640542382,
                    nft_name='88802726984',
                    nft_address='EQCu7UaREKnpfwzYBzUs6Aow7aQMz1c1DCPl5fWfE1OTMkuh',
                    address='EQDcN8gVIikHON6mLNN50NP2e5LIySKvHpkYrTfMh_TrNzFG',
                    tx_hash='1',
                ),
                UserNftWithdrawal(
                    user_id=6640542382,
                    nft_name='superhipe',
                    nft_address='EQAVfzSBSKU8oDY-cz-0RxACzkx6NZ9CNc-JejWmLQcLtywm',
                    address='EQDcN8gVIikHON6mLNN50NP2e5LIySKvHpkYrTfMh_TrNzFG',
                    tx_hash='2',
                ),
            ]
            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def add_user_market_orders():
        async with new_session() as session:
            rows = [
                MarketOrder(
                    user_id=6640542382,
                    action=MarketAction.BUY,
                    nft_name='kidswallet',
                    nft_address='EQBqg8_bpc3gVzrerc3gjonZOwXmDYW0jS4WgOdSjORsOAh_',
                    price=10,
                ),
                MarketOrder(
                    user_id=6640542382,
                    action=MarketAction.SELL,
                    nft_name='kidswallet',
                    nft_address='EQBqg8_bpc3gVzrerc3gjonZOwXmDYW0jS4WgOdSjORsOAh_',
                    price=15,
                ),
            ]
            session.add_all(rows)
            await session.commit()

    async def all(self):
        await self.add_const()
        await self.add_user()
        await self.add_number()
        await self.add_username()
        await self.add_user_number()
        await self.add_user_username()
        await self.add_user_deposits()
        await self.add_user_withdrawals()
        await self.add_user_swaps()
        await self.add_user_nft_deposits()
        await self.add_user_nft_withdrawals()
        await self.add_user_market_orders()
