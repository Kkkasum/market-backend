import aiohttp

from src.common import config, r

tokens = {'ton': 11419}


class TokenService:
    @staticmethod
    async def get_ton_to_usdt_price() -> float | None:
        price = await r.get('ton_to_usdt')
        if price:
            return float(price)

        ton_id = 11419

        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY,
        }
        params = {'id': ton_id}

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data'][str(ton_id)]['quote']['USD']['price']

                await r.setex(name='ton_to_usdt', value=token_price, time=20)

                return token_price

    @staticmethod
    async def get_usdt_to_ton_price() -> float | None:
        price = await r.get('usdt_to_ton')
        if price:
            return float(price)

        ton_id = 11419

        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY,
        }
        params = {'id': ton_id}

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data'][str(ton_id)]['quote']['USD']['price']
                if not token_price:
                    return

                await r.setex(name='usdt_to_ton', value=1 / token_price, time=20)

                return 1 / token_price

    @staticmethod
    async def get_usdt_to_rub_price() -> float | None:
        price = await r.get('usdt_to_rub')
        if price:
            return float(price)

        usdt_id = '825'

        url = ' https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY,
        }
        params = {'id': usdt_id, 'amount': 1, 'convert': 'RUB'}

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data']['quote']['RUB']['price']
                if not token_price:
                    return

                await r.setex(name='usdt_to_ton', value=1 / token_price, time=20)

                return 1 / token_price
