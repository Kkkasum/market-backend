import asyncio
import aiohttp

from pytonapi import AsyncTonapi

from src.common import config


async def main():
    client = AsyncTonapi(api_key=config.TONAPI_KEY, is_testnet=True)

    res = await client.webhooks.create_webhook(endpoint='https://useton.net/api/deposit/ton')
    webhook_id = res.webhook_id

    res = await client.webhooks.list_webhooks()
    print(res)

    res = await client.webhooks.subscribe_to_account(webhook_id=webhook_id, accounts=[config.TON_WALLET_ADDRESS])
    print(res)

    res = await client.webhooks.get_subscriptions(webhook_id=webhook_id)
    print(res)


if __name__ == '__main__':
    asyncio.run(main())
