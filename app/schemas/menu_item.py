from typing import Optional
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    category: str
    image: str #Need to figure out how to validate only image urls
    availability: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image: Optional[str] = None 
    availability: Optional[bool] = None