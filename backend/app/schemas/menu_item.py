from typing import Optional
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    category: str
    image: str #Need to figure out how to validate only image urls
    availability: bool = True
    description: Optional[str] = None

class ItemRead(ItemCreate):
    id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image: Optional[str] = None
    availability: Optional[bool] = None
    description: Optional[str] = None

# update_menu_item returns only the id plus the fields that were changed
class ItemUpdated(ItemUpdate):
    id: int
