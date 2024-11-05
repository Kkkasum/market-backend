from pydantic_settings import BaseSettings, SettingsConfigDict

from ._constants import BASE_DIR


class Config(BaseSettings):
    ORIGIN_URL: str

    IS_TESTNET: bool = False
    TONAPI_KEY: str
    TONCENTER_API_KEY: str
    TONCENTER_API_KEY_TESTNET: str

    CMC_API_KEY: str
    B2B_API_KEY: str

    ONLYPAYS_API_ID: str
    ONLYPAYS_SECRET_KEY: str

    MNEMONICS: str
    TON_WALLET_ADDRESS: str

    BOT_TOKEN: str
    ADMIN_ID: int

    PG_HOST: str
    PG_PORT: str
    PG_NAME: str
    PG_USER: str
    PG_PASS: str

    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def DB_URI(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env', env_file_encoding='utf-8', extra='ignore'
    )


config = Config()
