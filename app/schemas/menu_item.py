from typing import Optional
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    category: str
    image: str #Need to figure out how to validate only image urls
    availability: bool = True