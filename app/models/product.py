from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    title: str
    niche: Optional[str] = None
    cost: Optional[float] = None
    price: Optional[float] = None
    status: Optional[str] = "draft"
