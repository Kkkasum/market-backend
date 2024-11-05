from pydantic import BaseModel, Field


class Requisite(BaseModel):
    onlypays_id: str = Field(validation_alias='id')
    requisite: str
    owner: str
    bank: str
    payment_type: str
