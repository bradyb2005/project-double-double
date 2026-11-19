from pydantic import BaseModel, Field
from datetime import datetime



class OrderItem(BaseModel):
    item_id: int
    name: str
    price: float = Field(..., gt=0, description = "Price must be greater than 0")
    quantity: int = Field(..., gt=0, description = "Quantity must be greater than 0")

class Order(BaseModel):
    id: int
    customer_id: int
    customer_details: dict
    restaurant_id: int
    items: list[OrderItem]
    total_price: float = Field(..., gt=0, description = "Total price must be greater than 0")
    status: str = "pending"
    created_at: datetime
