from pydantic import BaseModel, Field


class WithdrawRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    address: str


class WithdrawUsdtRequest(WithdrawRequest):
    amount: float


class WithdrawTonRequest(WithdrawUsdtRequest):
    pass


class WithdrawNumberRequest(WithdrawRequest):
    number: str


class WithdrawUsernameRequest(WithdrawRequest):
    username: str
