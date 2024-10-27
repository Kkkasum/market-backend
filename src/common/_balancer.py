from pytoniq import LiteClient

MAINNET = LiteClient.from_mainnet_config(trust_level=2)
TESTNET = LiteClient.from_testnet_config(trust_level=2)
