from pydantic import BaseModel, Field


class DepositAddressResponse(BaseModel):
    deposit_address: str = Field(serialization_alias='depositAddress')


class DepositRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')


class DepositTokenRequest(DepositRequest):
    sender: str
    destination: str
    token: str
    amount: float


class DepositNumberRequest(DepositRequest):
    number: str


class DepositUsernameRequest(DepositRequest):
    username: str
