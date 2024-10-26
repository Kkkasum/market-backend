from pydantic import BaseModel, Field


class DepositAddressResponse(BaseModel):
    deposit_address: str = Field(serialization_alias='depositAddress')


class DepositTronRequest(BaseModel):
    id: str
    category: str
    coin: str
    full_amount: str
    fee: str
    address: str
    status: str
    tx_id: str
    created_at: int
    explorer_link: str
