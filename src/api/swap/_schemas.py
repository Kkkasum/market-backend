from pydantic import BaseModel, Field


class FeeResponse(BaseModel):
    fee: int | None


class AddSwapRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    from_token: str = Field(validation_alias='fromToken')
    from_amount: str = Field(validation_alias='fromAmount')
    to_token: str = Field(validation_alias='toToken')
