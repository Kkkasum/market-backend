from pydantic import BaseModel, Field


class FeeResponse(BaseModel):
    fee: int


class AddSwapRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    from_token: str = Field(validation_alias='fromToken')
    from_amount: float = Field(validation_alias='fromAmount')
    to_token: str = Field(validation_alias='toToken')
