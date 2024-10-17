from pytoniq import LiteBalancer


MAINNET = LiteBalancer.from_mainnet_config(trust_level=1)
TESTNET = LiteBalancer.from_testnet_config(trust_level=1)
