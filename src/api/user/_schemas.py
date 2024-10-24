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


class AddUserRequest(BaseModel):
    user_id: int = Field(validation_alias='userId')
