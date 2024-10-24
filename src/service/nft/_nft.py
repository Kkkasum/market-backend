from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


class NftService:
    @staticmethod
    async def get_nft_collection_floor_price(collection_address: str) -> float | None:
        transport = AIOHTTPTransport(url='https://api.getgems.io/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)

        async with client as session:
            query = gql(
                """
                query NftCollectionStats($address: String!) {
                    alphaNftCollectionStats(address: $address) {
                        floorPrice
                        itemsCount
                        totalVolumeSold
                    }
                    nftCollectionByAddress(address: $address) {
                        approximateHoldersCount
                    }
                }
                """
            )
            params = {
                'address': collection_address
            }
            res = await session.execute(query, variable_values=params)

            collection_stats = res['alphaNftCollectionStats'] | res['nftCollectionByAddress']

            return collection_stats.get('floorPrice', None)
