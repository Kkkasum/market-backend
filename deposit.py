import asyncio
from time import time

from src.common import config
from src.repo.account import AccountRepo
from src.service.account import AccountSubscription


async def start_subscription():
    start_utime = (await AccountRepo.get_start_utime()).start_utime
    if not start_utime:
        await AccountRepo.add_start_utime()
        start_utime = int(time())
    else:
        await AccountRepo.update_start_utime()

    account = AccountSubscription(address=config.TON_WALLET_ADDRESS, start_utime=int(start_utime.timestamp()))
    await account.check_for_deposit()

    print('Complete checking')


async def main():
    await start_subscription()
    await asyncio.sleep(30)

    return await main()


if __name__ == '__main__':
    asyncio.run(main())
