from pydantic import BaseModel

from src.repo.admin import CommissionType


class Commission(BaseModel):
    type: CommissionType
    value: float
