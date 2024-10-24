from pydantic import BaseModel

from src.repo.admin import FeeType


class Fee(BaseModel):
    type: FeeType
    value: float
