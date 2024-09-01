from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    description: str
    category: str
    quantity: int
    price: int


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    quantity: Optional[int] = Field(None)
    price: Optional[float] = Field(None)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    quantity: int
    price: int
