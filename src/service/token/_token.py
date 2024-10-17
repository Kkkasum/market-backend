import aiohttp

from src.common import config, r


tokens = {
    'ton': 11419
}


class TokenService:
    @staticmethod
    async def get_ton_to_usdt_price() -> float | None:
        price = await r.get('ton_to_usdt')
        if price:
            return float(price)

        url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY
        }
        params = {
            'id': 11419
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data'][str(11419)]['quote']['USD']['price']

                await r.setex(name='ton_to_usdt', value=token_price, time=20)

                return token_price

    @staticmethod
    async def get_usdt_to_ton_price() -> float | None:
        price = await r.get('usdt_to_ton')
        if price:
            return float(price)

        url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY
        }
        params = {
            'id': 11419
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data'][str(11419)]['quote']['USD']['price']
                if not token_price:
                    return

                await r.setex(name='usdt_to_ton', value=1 / token_price, time=20)

                return 1 / token_price

    @staticmethod
    async def get_token_price(token: str) -> float | None:
        token_id = tokens.get(token, None)
        if not token_id:
            return

        url = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.CMC_API_KEY
        }
        params = {
            'id': token_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()
                token_price = res['data'][str(token_id)]['quote']['USD']['price']

                return token_price
