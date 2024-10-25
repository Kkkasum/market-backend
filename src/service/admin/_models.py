from pydantic import BaseModel

from src.repo.admin import Const


class GetConst(BaseModel):
    const: Const
    value: float
