from pydantic import BaseModel, Field

from src.service.user import User, UserWallet, UserHistory
from src.service.number import Number
from src.service.username import Username


class UserResponse(User):
    pass


class UserWalletResponse(UserWallet):
    pass


class UserNumbersResponse(BaseModel):
    numbers: list[Number]


class UserUsernamesResponse(BaseModel):
    usernames: list[Username]


class UserHistoryResponse(UserHistory):
    pass


class AddUserSwapRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
    from_token: str = Field(validation_alias='fromToken')
    from_amount: float = Field(validation_alias='fromAmount')
    to_token: str = Field(validation_alias='toToken')
