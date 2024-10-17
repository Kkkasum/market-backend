from pydantic import BaseModel


class TokenRateResponse(BaseModel):
    token: str
    rate: str
