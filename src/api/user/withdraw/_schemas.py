from pydantic import BaseModel, Field


class WithdrawRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    address: str


class WithdrawTokenRequest(WithdrawRequest):
    token: str
    amount: float


class WithdrawNumberRequest(WithdrawRequest):
    number: str


class WithdrawUsernameRequest(WithdrawRequest):
    username: str
